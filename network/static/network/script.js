//Function que me permite agarrar el cookie para mandar fetchs con el csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

//A esta funcion me faltaria buscar el numero de followers y sumarle UNO igual WHATEVER brah
function un_follow(user_id){
    if($('#followBtn').hasClass('btn-primary')){
        //En este caso es follow
        $('#followBtn').removeClass('btn-primary').addClass('btn-danger').text('Unfollow');
        
        fetch('/follow', {
            method: 'POST',
            body:JSON.stringify({'action':'follow',
                                'user_id': user_id}),
            headers: {
                "X-CSRFToken": csrftoken
            }
          })
          .then(data => {
            //Tengo que agregar uno a los followers
            $('#followers').text(parseInt($('#followers').text()) + 1)
          })
      
    } else {
        //En este caso es unfollow
        $('#followBtn').removeClass('btn-danger').addClass('btn-primary').text('Follow');
        fetch('/follow', {
            method: 'POST',
            body:JSON.stringify({'action':'unfollow',
                                'user_id': user_id}), 
            headers: {
                "X-CSRFToken": csrftoken
            }
          })
          .then(data => {
            console.log(data)
            $('#followers').text(parseInt($('#followers').text()) - 1)
          })
    }
}


//Funcionabilidad 
//Creo que cada post tendria que tener un ID para saber cual es el que voy a UPDATEAR en el BACKEND

function editPost(){
    //Tengo que irme al Sibiling que tiene display None y cambiarle a Block y a esto se lo cambio a None
    $(event.target).css('display', 'none')
    $(event.target).siblings().css('display', 'block')

    //Ya voy al sibiling y hago el display. Ahora me tengo que ir al <p> y hacerlo textarea    
    var text = $(event.target).closest('.tweet-container').find('p:first').text()
    // Create a new textarea element
    var textarea = $("<textarea style='width: 550px; height: 70px;'></textarea>");
    textarea.val(text);
    //Replace el elemetn con el textarea elemetn que cree
    $(event.target).closest('.tweet-container').find('p:first').replaceWith(textarea);

}

//Con el Save lo que tengoq ue hacer es agarrar el TEXTCONTENT del TEXTAREa y mandarlo
//al view que sea y ahi lo guardo y transformo todo como estaba WAHTEVer.

function savePost(postId){
    //Agarro el TEXt
    text = $(event.target).closest('.tweet-container').find('textarea:first').val()
    //Tiene que hacer un fetch a la view que corresponda 
    //Lo hago ACÁ porque adentro no tengo even target

    //Saco el boton save y muestro el boton Edit
    $(event.target).css('display', 'none')
    $(event.target).siblings().css('display', 'block')


    //Cambio el TextArea por un paragraph

    // Create a new PARAgraph element
    var paragraph = $("<p></p>");
    paragraph.text(text);
    //Replace el elemetn con el textarea elemetn que cree
    $(event.target).closest('.tweet-container').find('textarea:first').replaceWith(paragraph);

    
    //Si todo sale OK oculto este boton, y muestro el otro de EDIT y cambio el TEXT AREA por PARAGRAPH
    fetch('/editPost', {
        method: 'POST',
        body:JSON.stringify({'postId': postId,
                            'text': text}), 
        headers: {
            "X-CSRFToken": csrftoken
        }
      })
        .then(data => {
            console.log(data)
            console.log(data.status)
            if (data.status == 200){
                showAlert('success', 'Post edited successfully')
            }else{
                showAlert('error', "You don't have permissions to edit")
            }

    })

}

function showAlert(tipo, mensaje){
    if (tipo == 'info'){
      tipo = '#infoAlert'
    } else if( tipo == 'success'){
      tipo = '#successAlert'
    } else if( tipo == 'error'){
      tipo = '#dangerAlert'
    }
  
    //Muestro el div
    $(tipo).show().delay(4500).fadeOut()
    //Cambio el text
    $(tipo).find('span').text(mensaje)
}

//LIKE or UNLIKE
function unLike(action, postId){
    console.log(action, postId)
}

//Lo que puedo hacer aca es que si tiene la clase: fa-regular -> unlike. Else -> Like
function un_like(postId){
    //Tengo que ver si EVENT.TARGET tiene ceirta clase

    console.log(event.target)
    
    if($(event.target).hasClass('fa-regular')){
        //En este caso es UNLIKE
        console.log('unlike!!!1')
        //Como es unlike tengo que transformar el boton y restarle un like al Span.
        $(event.target).removeClass('fa-regular').removeClass('fa').addClass('far').css('color', 'black');
        $(event.target).siblings('span').text(parseInt($(event.target).siblings('span').text()) - 1)
        
        
        fetch('/unLike', {
            method: 'POST',
            body:JSON.stringify({'action':'unlike',
                                'post_id': postId}),
            headers: {
                "X-CSRFToken": csrftoken
            }
          })
          .then(data => {
            console.log(data)
          })
    } else {
        //En este caso es Like
        console.log('LIKEEe')
        $(event.target).addClass('fa-regular').removeClass('far').addClass('fa').css('color', 'red');
        $(event.target).siblings('span').text(parseInt($(event.target).siblings('span').text()) + 1)

        fetch('/unLike', {
            method: 'POST',
            body:JSON.stringify({'action':'like',
                                'post_id': postId}), 
            headers: {
                "X-CSRFToken": csrftoken
            }
          })
          .then(data => {
            console.log(data)
          })
    }
}
