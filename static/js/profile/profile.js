              // image ---> validations
              let user_images=[]
              default_width=1000
              count=0 
              function tocheck_updates(){   
                  if (user_images.length!=0){
                      document.getElementById("profile_pic_pop_up_submit_div_btn").disabled=""
                      clearInterval(check_for_profie_img_loaded)
              }
              }

              document.querySelector("#profile_image_tag").addEventListener("click",function(){
                  check_for_profie_img_loaded=window.setInterval(tocheck_updates,2000)
              })
              document.querySelector("#close-profile-form").addEventListener("click",function(){
                  clearInterval(check_for_profie_img_loaded)
              })
              


              document.querySelector("#profile_pic_pop_up_submit_div_btn").addEventListener("click",(e)=>{
                  execute_upload()
              document.querySelector(".profile_pic_upload").classList.remove("upload")
              document.querySelector(".profile_main_div").classList.remove("click_on_profile_btn")
              window.location.reload()
              })
         
              function execute_upload(){

              console.log("user_images_len",user_images.length)
              for (a=0;a<user_images.length;a++)
              {
                  console.log("upload",user_images[a])
                  result = upload_img(user_images[a])
                  console.log("result",result)
              }
              } 

              // upload file 

           
              let upload_img = (file) =>{
              const url = "http://127.0.0.1:8000/profile/"
              let payload = new FormData()
              payload.append('profile_pic',file)
              // payload.append('user_email','{{user_email_id|safe}}')

              const csrfToken = document.cookie
              console.log("csrf", csrfToken)

              temppp=csrfToken.split(";")[0] 
              csrftoken=temppp.split("=")[1] 
              console.log("ssasa",csrftoken)
              const headers = new Headers({
                  // 'Accept': 'application/json',
                  // 'Content-Type': 'Content-type: image/jpeg; charset=UTF-8',
                  'X-CSRFToken': csrftoken
          });

              
              console.log("profile_pic : ",payload)
              fetch(url,{
                  method : 'POST',
                  headers,
                  body : payload

              })

              return 'success'

              }

              // on click POST AD send data images to be
              let imgae_file=document.querySelector("#upload_profile_pic_input").addEventListener("change",(e)=>

              
              {
           
              length=e.target.files.length
              console.log("length : ",length)
                  file=e.target.files[0]
                  image_instance=new FileReader
                  image_instance.readAsDataURL(file)
                  image_instance.onload = (e)=>
                      {
                          image_url=e.target.result
                          let image=document.createElement("img")
                          image.src=image_url
                  // document.getElementById("div_empty1").appendChild(image)
                          image.onload=(e)=>
                          {
                          let canvas = document.createElement("canvas")
                          let ratio=default_width / e.target.width
                          canvas.width=default_width
                          canvas.height=e.target.height * ratio
                          const context=canvas.getContext("2d")
                          context.drawImage(image,0,0,canvas.width,canvas.height)
                          // let new_img_url=context.canvas.toDataURL("image/jpeg",90)
                          let new_img_url=context.canvas.toDataURL("image/jpeg",100)
                          let image_file=urlToFile(new_img_url)
                          console.log("image_file : ",image_file)
                          user_images[0]=(image_file[0])

                          
                         
                  // upload_img(image_file)
                      // display_selected_images
                      // image_inst=new FileReader
                      // console.log("user_image",user_images)
                      // image_inst.readAsDataURL(user_images[a])
                      // image_inst.onload = (e)=>{
                      // image_URL=e.target.result
                          // }
                      }  
                        
                  } 
              })
              urlToFile = (url) =>{
              let arr=url.split(",")
              let mime = arr[0].match(/:(.*?);/)[1]
              let data = arr[1]
              // decode the data
              let datastr =atob(data)
              len=datastr.length
              let dataArr = new Uint8Array(len)
              while(len--)
              {
                  dataArr[len] = datastr.charCodeAt(len)
              }
              file = new File([dataArr],count+'.jpeg',{type: mime})
              console.log("file_name",file)
              count++;
              // console.log("data : ",file)
              // let send = document.getElementById("user_images")
              return [file]
        
              }