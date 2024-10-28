function sendMail(){
    let parms ={
        name : document.getElementById("name").value,
        email : document.getElementById("email").value,
        message : document.getElementById("message").value,

    }

    emailjs.send("service_kht8nph","template_nx33q4r",parms)
}