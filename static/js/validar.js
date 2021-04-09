
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("formulario").addEventListener('submit', validarFormulario); 
});
function validarFormulario(evento) {
    evento.preventDefault();
    let Name = document.getElementById('Name').value;
    if(Name.length == 0) {
        alert('[ERROR] El campo Nombre debe tener un valor ...');
        return false;
        
    }
    // let email = document.getElementById('email').value;
    // let email= /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    // Se muestra un texto a modo de ejemplo, luego va a ser un icono
    // if (email.test(campo.value)) {
    //     alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
    //     return;
    // } 
    // let email = document.getElementById('email').value;
    // if ((strlen(email) >= 6) && (substr_count(email,"@") == 1) && (substr(email,0,1) != "@") && (substr(email,strlen(email)-1,1) != "@")){
    //     if ((!strstr(email,"'")) && (!strstr(email,"\"")) && (!strstr(email,"\\")) && (!strstr(email,"\$")) && (!strstr(email," "))) {
    //         alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
    //     return; 
    // }
    // if (email('/^[^0-9][a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[@][a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,4}$/', "mi.email.correcto@gmail.com")) {
    //     alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
    //     return; 
    // }
     
    // if (email('/^[^0-9][a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[@][a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,4}$/', "mi.email.incorrecto")) {
    //     alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
    //     return;
    // }
    // let email = document.getElementById('email').value;
    // if(email !== '@'){
    //     alert('Algo del numero del correo electronico no esta correcto, vuelva a revisarlos');
    //     return; 
    // }
    // let email = document.getElementById('email').value;
    // if (!/[a-z]/.test(email) || !/[A-Z]/.test(email) || !/[@]{1}/.test(email) ){
    //     alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
    //     return;
    // }
    let Identification = document.getElementById('Identification').value;
    if(Identification.length !== 9){
        alert('Algo del numero de la identificacion no esta correcto, vuelva a revisarlos');
        return;
    }
    let City = document.getElementById('City').value;
    if(City.length == 0) {
        alert('[ERROR] El campo Cuidad debe tener un valor de...');
        return;
    }
    let Country = document.getElementById('Country').value;
    if(Country.length == 0) {
        alert('[ERROR] El campo Pais debe tener un valor de...');
        return;
    }
    let Password = document.getElementById('Password').value;
    if (!/[a-z]/.test(Password) || !/[A-Z]/.test(Password) || !/[0-9]{1}/.test(Password) || Password.length < 7) {
        alert("El campo 'Contrasena' no es correcto. Es obligatorio, de minimo 7 caracteres, y debe contener una mayuscula, una minuscula y un digito");
        return;
    this.submit();
    }
}

$('.carousel').carousel({
    interval: 2000
})


// function email($str)
// {
//   $matches = null;
//   return (1 === preg_match('/^[A-z0-9\\._-]+@[A-z0-9][A-z0-9-]*(\\.[A-z0-9_-]+)*\\.([A-z]{2,6})$/', $str, $matches));
// }
// function validarFormulario(email){
//     email_correcto = 0;
//     //compruebo unas cosas primeras
//     if ((strlen($email) >= 6) && (substr_count($email,"@") == 1) && (substr($email,0,1) != "@") && (substr($email,strlen($email)-1,1) != "@")){
//        if ((!strstr($email,"'")) && (!strstr($email,"\"")) && (!strstr($email,"\\")) && (!strstr($email,"\$")) && (!strstr($email," "))) {
//           //miro si tiene caracter .

//           if (substr_count($email,".")>= 1){
//              //obtengo la terminacion del dominio
//              $term_dom = substr(strrchr ($email, '.'),1);
//              //compruebo que la terminación del dominio sea correcta
//              if (strlen($term_dom)>1 && strlen($term_dom)<5 && (!strstr($term_dom,"@")) ){
//                 //compruebo que lo de antes del dominio sea correcto
//                 $antes_dom = substr($email,0,strlen($email) - strlen($term_dom) - 1);
//                 $caracter_ult = substr($antes_dom,strlen($antes_dom)-1,1);
//                 if ($caracter_ult != "@" && $caracter_ult != "."){
//                    $mail_correcto = 1;
//                    alert('Algo del correo electronico no esta correcto, vuelva a revisarlos');
//                 }
//              }
//           }
//        }
//     }
//     if ($mail_correcto)
//        return 1;
//     else
//        return 0;
