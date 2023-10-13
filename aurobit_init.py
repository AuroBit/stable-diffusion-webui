import urllib.request
import os

from git import repo


# download models
sd_models = [
    "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/beautifulRealistic_brav5.safetensors",
    "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/majicmixRealistic_v5.safetensors",
    "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/realisticVisionV51_v51VAE-inpainting.safetensors"
]
sd_path = 'models/Stable-diffusion'
for model_file in sd_models:
    base_name = os.path.basename(model_file)
    dl_path = f'{sd_path}/{base_name}'
    if not os.path.exists(dl_path):
        print(f'Downloading model: {model_file}')
        urllib.request.urlretrieve(model_file, dl_path)
    else:
        print(f'Model exist: {model_file}')
    print(f'Download model DONE: {model_file}')


# extensions
ext_git_path = {
    "sd-webui-controlnet": "https://github.com/Mikubill/sd-webui-controlnet",      # controlnet
    "adetailer": "https://github.com/Bing-su/adetailer.git",             # adtailer
    # "sd-weibui-inpaint-anything": "https://github.com/Uminosachi/sd-webui-inpaint-anything.git"
}
ext_path = 'extensions'
for repo_name, rep_path in ext_git_path.items():
    try:
        local_path = f'{ext_path}/{repo_name}'
        print(f'Cloning repo from: {rep_path}')
        print(f'    to: {local_path}')
        repo.Repo.clone_from(rep_path, local_path)
    except Exception as e:
        print(f'Clone {rep_path} FAIL.  repo exist or network error.')
        print(e.args)
    print(f'Clone repo DONE: {rep_path}')


# download control net model
control_net_dir = f'{ext_path}/sd-webui-controlnet'
controlnet_models = [
    "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/controlnet_models/control_v11f1p_sd15_depth.pth",
    "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/controlnet_models/control_v11p_sd15_canny.pth"
]
cn_model_dir = f'{control_net_dir}/models'
if os.path.exists(control_net_dir):
    for model_file in controlnet_models:
        base_name = os.path.basename(model_file)
        local_path = f'{cn_model_dir}/{base_name}'
        if not os.path.exists(local_path):
            print(f'Downloading controlnet: {model_file}')
            urllib.request.urlretrieve(model_file, local_path)
        else:
            print(f'Controlnet exist: {model_file}')
        print(f'Download controlnet DONE: {model_file}')
        

            
        
    

