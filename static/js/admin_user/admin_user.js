const Previous_posted_info = JSON.parse(document.getElementById('new_script').textContent);
console.log("data",Previous_posted_info)

var copy_clicked=document.querySelector("#func_check_to_copy")
copy_clicked.addEventListener("change",(e)=>{

if (e.target.checked){

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

document.getElementById("parking_select").value="" 

}else{
    console.log("Clicked and false")
    document.getElementById("selling_submit_btn2").click()
}
})
