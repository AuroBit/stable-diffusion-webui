import urllib.request
import os
import argparse
import shutil
import time

from git import repo


# parse arguments
parser = argparse.ArgumentParser()

parser.add_argument('-cache', default='yes', help="This is argument 1")
parser.add_argument('-s3', default='yes', help="This is argument 2")

args = parser.parse_args()
cache_resource = True if args.cache == 'yes' else False
use_s3 = True if args.s3 == 'yes' else False

print(f"Cache resource: {cache_resource}")
print(f"Use S3: {use_s3}")

cache_dir = "/workspace/sd_resource"
failed_retry = 5

resource_path = {
    "tencent": {
        "sd_models": [
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/beautifulRealistic_brav5.safetensors",
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/majicmixRealistic_v5.safetensors",
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_models/realisticVisionV51_v51VAE-inpainting.safetensors"
        ],
        "sd_lora": ["https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_lora/meiyan_V1.safetensors"],
        "controlnet_models": [
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/controlnet_models/control_v11f1p_sd15_depth.pth",
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/controlnet_models/control_v11p_sd15_canny.pth"
        ],
        "ad_ext_models": [
            "https://aiyo-1319341997.cos.ap-nanjing.myqcloud.com/common_resource/sd_other/sow_pyramid_a5_e3d2_remapped.pth"
        ]
    },
    
    "s3": {
        "sd_models": [
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/sd_models/beautifulRealistic_brav5.safetensors",
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/sd_models/majicmixRealistic_v5.safetensors",
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/sd_models/realisticVisionV51_v51VAE-inpainting.safetensors"
        ],
        "sd_lora": ["https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/lora/meiyan_V1.safetensors"],
        "controlnet_models": [
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/controlnet/control_v11f1p_sd15_depth.pth",
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/controlnet/control_v11p_sd15_canny.pth"
        ],
        "ad_ext_models": [
            "https://aurobit-s3-01.s3.ap-northeast-1.amazonaws.com/common_resource/sd/sd_others/sow_pyramid_a5_e3d2_remapped.pth"
        ]
    },
}


def ab_download_resource(url, file_dir):
    base_name = os.path.basename(url)
    
    # make target dir
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    
    # cache resource
    if cache_resource:
        # download to cache dir
        file_cache_dir = f'{cache_dir}/{file_dir}'
        file_cache_path = f'{file_cache_dir}/{base_name}'
        if not os.path.exists(file_cache_dir):
            os.makedirs(file_cache_dir)
        if not os.path.exists(file_cache_path):
            _start_time = time.time()
            urllib.request.urlretrieve(url, file_cache_path)
            _end_time = time.time()
            print(f'[Download to cache] {url} -> {file_cache_path}')
            print("Elapsed time: {:.2f} seconds".format(_end_time - _start_time))
        else:
            print(f'[Download to cache] file exists: {file_cache_path}')
            
        # copy from cache
        file_path = f'{file_dir}/{base_name}'
        if not os.path.exists(file_path):
            shutil.copy(file_cache_path, file_path)
            print(f'[Copy from cache] {file_cache_path} -> {file_path}')
        else:
            print(f'[Copy from cache] file exists: {file_path}')
        
    # download directly
    else:
        file_path = f'{file_dir}/{base_name}'
        if not os.path.exists(file_path):
            _start_time = time.time()
            urllib.request.urlretrieve(url, file_path)
            _end_time = time.time()
            print(f'[Download directly] {url} -> {file_path}')
            print("Elapsed time: {:.2f} seconds".format(_end_time - _start_time))
            
        else:
            print(f'[Download directly] file exists: {file_path}')
            

try_cnt = failed_retry
while try_cnt > 0:
    try_cnt = try_cnt - 1
    
    try:
        # ==================== prepare extensions ============================

        ext_git_path = {
            "sd-webui-controlnet": "https://github.com/Mikubill/sd-webui-controlnet",      # controlnet
            # "adetailer": "https://github.com/Bing-su/adetailer.git",             # adtailer
            "adetailer": "https://github.com/AuroBit/adetailer.git",
            # "sd-weibui-inpaint-anything": "https://github.com/Uminosachi/sd-webui-inpaint-anything.git"
            # "sd-webui-animatediff": "https://github.com/continue-revolution/sd-webui-animatediff.git"
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

            
            

        # ====================== prepare resource =================================

        all_resource = resource_path["s3"] if use_s3 else resource_path["tencent"]
        sd_path = 'models/Stable-diffusion'
        sd_lora_path = 'models/Lora'
        control_net_dir = f'{ext_path}/sd-webui-controlnet/models'
        ad_rel_model_dir = f"models/adetailer"


        # download models
        print(f'************ Download SD models ********************')
        sd_models = all_resource["sd_models"]
        for model_file in sd_models:
            ab_download_resource(model_file, sd_path)


        # download loras
        print(f'************* Download Lora ******************')
        sd_lora = all_resource["sd_lora"]
        for model_file in sd_lora:
            ab_download_resource(model_file, sd_lora_path)


        # download control net model
        print(f'************* Download controlnet models ******************')
        controlnet_models = all_resource["controlnet_models"]
        if os.path.exists(control_net_dir):
            for model_file in controlnet_models:
                ab_download_resource(model_file, control_net_dir)

        # download ad-relative models
        print(f'************* Download ad-relative models ******************')
        ad_rel_models = all_resource["ad_ext_models"]
        for md_url in ad_rel_models:
            ab_download_resource(md_url, ad_rel_model_dir)
            
        break    
    
    except Exception as e:
        print(f"Exception: {e}")
            
        
    

