document.getElementById("div1").style="position:fixed; z-index:2"
let user_images=[]




// on click POST AD send data images to be
document.getElementById("confirm_btns").addEventListener("click",function(){
  
    for (a=0;a<length;a++)
    {
        result = upload_img(user_images[a])
        
    }

    document.querySelector(".comfirm_selection_btn").classList.remove('active')
    document.querySelector(".image_selected_div").classList.remove('active')
    document.body.style="overflow:scroll;"
    document.querySelector("#main_Div_selling_page").style="pointer-events: all ; opacity: 100%;"


})

document.getElementById("cancel_btns").addEventListener("click",function(){

    document.getElementById("selling_form").reset()
    document.querySelector(".comfirm_selection_btn").classList.remove('active')
    document.querySelector(".image_selected_div").classList.remove('active')
    document.body.style="overflow:scroll;"
    document.querySelector("#main_Div_selling_page").style="pointer-events: all ; opacity: 100%;"
    document.getElementById("user_images").disabled = false
    // location.reload()
    user_images=[]
    var element = document.getElementById("selected");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }  

})
    



default_width=1000
count=0    

let imgae_file=document.querySelector("#user_images").addEventListener("change",(e)=>
{

    length=e.target.files.length
    if (length<14){
        document.getElementById("user_images").disabled = true

    for(let a=0;a<length;a++)
    {
        file=e.target.files[a]
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

                user_images[a]=(image_file[0])

                console.log("user_images_len : ",user_images.length)

                if (user_images.length==length){
                    document.querySelector(".comfirm_selection_btn").classList.add("active")
                }
                

        // upload_img(image_file)

            // display_selected_images

            reference_div=document.querySelector(".image_selected_div");
            reference_div.classList.add('active');
            document.querySelector("#main_Div_selling_page").style="pointer-events: none ; opacity: 20%;"
            document.body.style="overflow:hidden;"
            image_inst=new FileReader
            console.log("user_image",user_images)
            image_inst.readAsDataURL(user_images[a])
            image_inst.onload = (e)=>{
            image_URL=e.target.result
            let display_img=document.createElement("img")
            display_img.src=image_URL
            display_img.classList='selected_img'
            reference_div.appendChild(display_img);

            }
             }
            }


    }

    }else{
        document.getElementById("user_images").value=""
        alert("You can only upload a maximum of 14 files")


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

    return [file,data]

 

}


// upload file 

let upload_img = (file) =>{
    const url = "http://127.0.0.1:8000/sell/images/"

    let payload = new FormData()

    payload.append('temp',file)

//     const csrfToken = document.cookie
//     console.log("csrf", csrfToken)

//     temppp=csrfToken.split(";")[0] 
//     csrftoken=temppp.split("=")[1] 
//     console.log("ssasa",csrftoken)
//     const headers = new Headers({
//         'Accept': 'application/json',
//         'Content-Type': 'application/json; charset=UTF-8',
//         'X-CSRFToken': csrftoken
// });

    fetch(url,{
        method : 'POST',
        // headers,
         body : payload
    
    })

return 'success'
}

// ===========Validations code==================
function validate(content,format){
    var content_format= new Object()
    console.log("format is : ",format)
    content_format= {
        "property_name": "^[a-zA-Z ]+$",
        "property_pincode": "^[1-9][0-9]{5}$",   
        "property_floor": "^[0-9]+$",
        "house_area" : "^[0-9]{1,9}$",
        "property_city": "^[a-zA-Z ]+$",
        "monthly_rent": "^[0-9]{1,9}$",
        "temp": "^[0-9]+$"
    }

    re=new RegExp(content_format[format])

    console.log("re",re)
    console.log("content : ",content)
    
    result=re.test(content)

    return result


    console.log("Result : ",result)
    

}    

function validate_creds(id,name){
   var check=document.getElementById(id).value
   result=validate(check,name)
//    console.log("Type : ",name)
//    console.log("op",result)
   if (check){
            if (result){
                document.getElementById(id).style=""

                
            }else{
                document.getElementById(id).style="outline:3px solid red"
              
                
            }
    }
   console.log("check : ",check)

    id1=document.getElementById("property_owner_name_div").style.outlineColor
    id2=document.getElementById("property_city_div").style.outlineColor
    id3=document.getElementById("property_pincode_div").style.outlineColor
    id4=document.getElementById("property_floor_div").style.outlineColor
    id5=document.getElementById("property_squareft_div").style.outlineColor
    id6=document.getElementById("property_monthly_rent_div").style.outlineColor
    // id7=document.getElementById("confimr_password").style.outlineColor


    if (id1 || id2 || id3 || id4 || id5 || id6){
    submit=document.getElementById("selling_submit_btn")
    submit.disabled="disabled"
    submit.style="background-color:#616161;cursor: not-allowed;"
    }else{
    submit=document.getElementById("selling_submit_btn")
    submit.disabled=""
    submit.style=""
    }

}

