function updateClock(){
  document.getElementById("clock").textContent=new Date().toLocaleTimeString();
}
setInterval(updateClock,1000);updateClock();
