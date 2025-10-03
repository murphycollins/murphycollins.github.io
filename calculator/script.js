function press(val){document.getElementById("calc-screen").value+=val;}
function calculate(){
  const screen=document.getElementById("calc-screen");
  try{screen.value=eval(screen.value);}catch{screen.value="Error";}
}
function clearScreen(){document.getElementById("calc-screen").value="";}
