const modal_elem = document.getElementById('modal');

function ChangeModalStatus(){
    console.log('ChangeModal executed');
    if (modal_elem.hasAttribute('class', 'hidden')){
        modal_elem.removeAttribute('class');
    } else {
        modal_elem.setAttribute('class', 'hidden');
    }
    
}