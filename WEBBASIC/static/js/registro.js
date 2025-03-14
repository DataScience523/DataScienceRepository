document.getElementById('my-form').addEventListener('submit',function(){
     
    var nombre = document.getElementById ('nombre').value;
    var apellido = document.getElementById('apellido').value;
    var correo = document.getElementById('email').value;

    if(nombre ===''|| apellido ==='' || correo===''){

        alert("ingresa los datos en la casilla")
    }else(
        alert("ingresaste los datos, gracias por registrarte")
    )


});
