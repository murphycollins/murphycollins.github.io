function addTask(){
  const input=document.getElementById("todo-input");
  const list=document.getElementById("todo-list");
  if(input.value.trim()!==""){
    const li=document.createElement("li");
    li.textContent=input.value;
    li.onclick=()=>li.remove();
    list.appendChild(li);
    input.value="";
  }
}
