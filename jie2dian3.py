from diffusers import PaintByExamplePipeline
import diffusers
import torch,torchvision
import nodes
import comfy.utils,comfy.samplers

topil = torchvision.transforms.ToPILImage()
totensor = torchvision.transforms.ToTensor()
InterpMode = torchvision.transforms.InterpolationMode

if(torch.cuda.is_available()):
    device = 'cuda'
elif(torch.backends.mps.is_available()):
    device = 'mps'
else:
    device = 'cpu'

interp_dic = {
    'bicubic': InterpMode.BICUBIC,
    'bilinear': InterpMode.BILINEAR,
    'lanczos': InterpMode.LANCZOS,
    'nearest': InterpMode.NEAREST,
    'nearest-exact': InterpMode.NEAREST_EXACT,
}

scheduler_dic = {
    'pndm': diffusers.PNDMScheduler,
    'euler': diffusers.EulerDiscreteScheduler,
    'euler_ancestral': diffusers.EulerAncestralDiscreteScheduler,
    'heun': diffusers.HeunDiscreteScheduler,
    'dpmpp_sde': diffusers.DPMSolverSDEScheduler,
    'lms': diffusers.LMSDiscreteScheduler,
    'ddpm': diffusers.DDPMScheduler,
    'lcm': diffusers.LCMScheduler,
    'ipndm': diffusers.IPNDMScheduler,
    'ddim': diffusers.DDIMScheduler,
    'uni_pc': diffusers.UniPCMultistepScheduler,
}

required_simple = {
    'image': ('IMAGE',),
    'mask': ('MASK',),
    'example': ('IMAGE',),
    'seed': ('INT:seed',{'min': 0,'max': 0xffffffffffffffff}),
    'steps': ('INT',{'default': 30,'min': 1}),
}

required_advanced = {
    **required_simple,
    'cfg': ('FLOAT',{'default': 5,'min': 0,'step': 0.1}),
    'sampler_name': (list(scheduler_dic),),
    'negative': ('STRING',{'multiline': True,'default': ''}),
    'resize': ('BOOLEAN',{'default': False}),
    'width': ('INT',{'default': 512,'min': 8,'step': 8}),
    'height': ('INT',{'default': 512,'min': 8,'step': 8}),
    'resize_mode': (list(interp_dic),)
}

required_gen = {
    'image': ('IMAGE',),
    'mask': ('MASK',),
    'model': ('MODEL',),
    'seed': ('INT:seed',{'min': 0,'max': 0xffffffffffffffff}),
    'steps': ('INT',{'default': 30,'min': 1}),
    'cfg': ('FLOAT',{'default': 5,'min': 0,'step': 0.1}),
    'sampler_name': (comfy.samplers.KSampler.SAMPLERS,),
    'scheduler': (comfy.samplers.KSampler.SCHEDULERS,),
    'positive': ('CONDITIONING',),
    'negative': ('CONDITIONING',),
    'latent_image': ('LATENT',),
    'vae': ('VAE',)
}

def callback(steps):
    pbar = comfy.utils.ProgressBar(steps)
    def f(step: int,timestep: int,latents: torch.FloatTensor):
        pbar.update(1)
    return f



class PaintbyExampleSimple:
    def __init__(self):            
        self.pipe = PaintByExamplePipeline.from_pretrained(
            'Fantasy-Studio/Paint-by-Example',
            torch_dtype=torch.float16,
        ).to(device)
        
    @classmethod
    def INPUT_TYPES(s):
        return {'required': required_simple}
    
    RETURN_TYPES = ('IMAGE',)
    FUNCTION = 'inpaint'
    CATEGORY = 'inpaint'
    
    def inpaint(self,image,mask,example,seed,steps):
        generator = torch.Generator(device).manual_seed(seed)
        n = max(len(image),len(example),len(mask))
        outimg = torch.Tensor(n,image.shape[1],image.shape[2],image.shape[3])
        for i in range(n):
            pil_example = topil(example[min(i,len(example)-1)].permute(2,0,1))
            pil_image = topil(image[min(i,len(image)-1)].permute(2,0,1))
            pil_mask = topil(mask[min(i,len(mask)-1)])
            if(pil_mask.size!=pil_image.size):
                pil_mask = pil_mask.resize(pil_image.size)
            
            pil_outimg = self.pipe(
                example_image=pil_example,
                image=pil_image,
                mask_image=pil_mask,
                num_inference_steps=steps,
                generator=generator,
                callback=callback(steps)
            ).images[0]
            
            outimg[i] = totensor(pil_outimg).permute(1,2,0)
        return (outimg,)


class PaintbyExampleAdvanced(PaintbyExampleSimple):
    @classmethod
    def INPUT_TYPES(s):
        return {'required': required_advanced}
    
    def inpaint(self,image,mask,example,seed,steps,cfg,sampler_name,negative,resize,width,height,resize_mode):
        example = example.permute(0,3,1,2)
        image = image.permute(0,3,1,2)
        mask = mask.unsqueeze(1)
        
        if(resize):
            resize_f = torchvision.transforms.Resize(size=(height,width),interpolation=interp_dic[resize_mode])
            image = resize_f(image)
            mask = resize_f(mask)
        else:
            resize_f = torchvision.transforms.Resize(size=image.shape[2:],interpolation=interp_dic[resize_mode])
            mask = resize_f(mask)
        
        generator = torch.Generator(device).manual_seed(seed)
        scheduler = scheduler_dic.get(sampler_name,'pndm')
        self.pipe.scheduler = scheduler.from_config(self.pipe.scheduler.config)
        
        n = max(len(image),len(example),len(mask))
        outimg = torch.Tensor(n,image.shape[1],image.shape[2],image.shape[3])
        for i in range(n):
            pil_example = topil(example[min(i,len(example)-1)])
            pil_image = topil(image[min(i,len(image)-1)])
            pil_mask = topil(mask[min(i,len(mask)-1)])
            
            pil_outimg = self.pipe(
                example_image=pil_example,
                image=pil_image,
                mask_image=pil_mask,
                num_inference_steps=steps,
                negative_prompt=negative,
                guidance_scale=cfg,
                generator=generator,
                callback=callback(steps)
            ).images[0]
            outimg[i] = totensor(pil_outimg)
            
        outimg = outimg.permute(0,2,3,1)
        return (outimg,)


class PaintbyExampleGen(PaintbyExampleAdvanced):
    @classmethod
    def INPUT_TYPES(s):
        return {'required': required_gen}

    RETURN_TYPES = ('IMAGE','IMAGE')
    RETURN_NAMES = ('image','example')
    FUNCTION = 'inpaintgen'
    
    def inpaintgen(self,image,mask,model,seed,steps,cfg,sampler_name,scheduler,positive,negative,latent_image,vae):
        lat = nodes.common_ksampler(model,seed,steps,cfg,sampler_name,scheduler,positive,negative,latent_image,denoise=1)
        example = vae.decode(lat[0]['samples'])
        return self.inpaint(image,mask,example,seed,steps,cfg,sampler_name,negative,False,0,0,'bicubic') + (example,)


int_req1 = ('INT',{'default': 255,'min': 0,'max': 255})
int_req2 = ('INT',{'default': 192,'min': 0,'max': 255})
int_req3 = ('INT',{'default': 16,'min': 1,'max': 1024})

class PaintbySingleColor:
    @classmethod
    def INPUT_TYPES(s):
        req = {
            'image': ('IMAGE',),
            'mask': ('MASK',),
            'red': int_req1,
            'green': int_req1,
            'blue': int_req1,
        }
        return {'required': req}
    
    RETURN_TYPES = ('IMAGE',)
    FUNCTION = 'inpaint'
    CATEGORY = 'inpaint'
    
    def fill(self,image,mask,imgfill):
        if(mask.shape[1:]!=image.shape[1:3]):
            resize_f = torchvision.transforms.Resize(size=image.shape[1:3],interpolation=InterpMode.BILINEAR)
            mask = resize_f(mask)
        outimg = image*(1-mask[:,:,:,None]) + imgfill*mask[:,:,:,None]
        return outimg
    
    def inpaint(self,image,mask,red,green,blue):
        imgfill = torch.clip(torch.FloatTensor([red,green,blue]).tile([*image.shape[:3],1])/255,0,1)
        return (self.fill(image,mask,imgfill),)


class PaintbyIchimatsu(PaintbySingleColor):
    @classmethod
    def INPUT_TYPES(s):
        req = {
            'image': ('IMAGE',),
            'mask': ('MASK',),
            'red1': int_req1,
            'green1': int_req1,
            'blue1': int_req1,
            'red2': int_req2,
            'green2': int_req2,
            'blue2': int_req2,
            'size_x': int_req3,
            'size_y': int_req3,
        }
        return {'required': req}
    
    def inpaint(self,image,mask,red1,green1,blue1,red2,green2,blue2,size_x,size_y):
        mx,my = torch.meshgrid(torch.arange(image.shape[2]),torch.arange(image.shape[1]))
        mz = ((mx%(size_x*2)<size_x) != (my%(size_y*2)<size_y))[:,:,None]
        imgfill = (mz*torch.Tensor([red1,green1,blue1]) + ~mz*torch.Tensor([red2,green2,blue2]))/255
        return (self.fill(image,mask,imgfill),)



NODE_CLASS_MAPPINGS = {
    'PaintbyExampleSimple': PaintbyExampleSimple,
    'PaintbyExampleAdvanced': PaintbyExampleAdvanced,
    'PaintbyExampleGen': PaintbyExampleGen,
    'PaintbySingleColor': PaintbySingleColor,
    'PaintbyIchimatsu': PaintbyIchimatsu,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    'PaintbyExampleSimple': 'Paint by Example (simple)',
    'PaintbyExampleAdvanced': 'Paint by Example (advanced)',
    'PaintbyExampleGen': 'Paint by Generated Example',
    'PaintbySingleColor': 'Paint by Single Color',
    'PaintbyIchimatsu': 'Paint by Ichimatsu',
}