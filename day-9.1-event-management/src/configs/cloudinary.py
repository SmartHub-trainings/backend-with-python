import cloudinary
from settings.environment import ENVS
# import cloudinary.uploader     
cloudinary.config( 
    cloud_name =ENVS.CLOUDINARY_CLOUD_NAME.value,
    api_key = ENVS.CLOUDINARY_API_KEY.value,
    api_secret =  ENVS.CLOUDINARY_API_KEY_SECRET.value,
    secure=True
)

# # Upload an image
# upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#                                            public_id="sh