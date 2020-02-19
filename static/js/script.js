let colorInput = document.queryselection('#color');
let hex = document.queryselection('#hex');

colorInput.addEventListener('input',() =>{
    let color = colorInput.value;
    hexInput.value = color;
    document.body.style.backgroundColor = color;
});