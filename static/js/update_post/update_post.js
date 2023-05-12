const Previous_posted_info = JSON.parse(document.getElementById('new_script').textContent);
console.log("data",Previous_posted_info)
if (Previous_posted_info){
document.getElementById("property_owner_name_div").value= Previous_posted_info.property_name
document.getElementById("property_type_select").value=Previous_posted_info.property_type.charAt(0).toUpperCase() + Previous_posted_info.property_type.slice(1)

// document.getElementById("property_distict_select").value=Previous_posted_info.property_distict".charAt(0).toUpperCase() + Previous_posted_info.property_distict".slice(1)
// document.getElementById("property_state_select").value=Previous_posted_info.property_state".charAt(0).toUpperCase() + Previous_posted_info.property_state".slice(1)
// document.getElementById("property_city_div").value=Previous_posted_info.property_city"
// document.getElementById("property_pincode_div").value=Previous_posted_info.property_pincode"
document.getElementById("property_floor_div").value=Previous_posted_info.property_floor

document.getElementById("property_rooms_select").value=Previous_posted_info.rooms.charAt(0).toUpperCase() + Previous_posted_info.rooms.slice(1)

document.getElementById("property_squareft_div").value=Previous_posted_info.house_area

document.getElementById("furnished_or_semi_select").value=Previous_posted_info.furnished_or_semi.charAt(0).toUpperCase() + Previous_posted_info.furnished_or_semi.slice(1)

document.getElementById("appliance_tv").checked=Previous_posted_info.appliance_TV==true?"checked":""

document.getElementById("appliance_fridge").checked=Previous_posted_info.appliance_Fridge==true?"checked":""
document.getElementById("appliance_sofa").checked=Previous_posted_info.appliance_sofa==true?"checked":""

document.getElementById("appliance_bed").checked=Previous_posted_info.appliance_bed==true?"checked":""

document.getElementById("appliance_dresser").checked=Previous_posted_info.appliance_dresser==true?"checked":""
document.getElementById("appliance_ac").checked=Previous_posted_info.appliance_AC==true?"checked":""
document.getElementById("appliance_washing_machine").checked=Previous_posted_info.appliance_washing_machine==true?"checked":""
document.getElementById("appliance_water_heater").checked=Previous_posted_info.appliance_water_heaters==true?"checked":""
document.getElementById("appliance_water_purifier").checked=Previous_posted_info.appliance_water_purifier==true?"checked":""
document.getElementById("appliance_fan").checked=Previous_posted_info.appliance_fans==true?"checked":""
document.getElementById("appliance_tubelights").checked=Previous_posted_info.appliance_tubelights==true?"checked":""
document.getElementById("appliance_Inventers").checked=Previous_posted_info.appliance_Inventers==true?"checked":""
document.getElementById("property_monthly_rent_div").value=Previous_posted_info.monthly_rent
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


function checkbox_btn_click(input_id,id) {
    element=document.getElementById(input_id).click();

};

const Property_updated_success=JSON.parse(document.getElementById("updated_popup").textContent)
console.log("Property_updated_success : " + Property_updated_success)
if (Property_updated_success){
    product_updated_pop_up()
}
function product_updated_pop_up(){
    alert("POST UPDATED")
    window.location.href="/profile/"
}