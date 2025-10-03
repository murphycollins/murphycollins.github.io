new Chart(document.getElementById("chart"),{
  type:'bar',
  data:{
    labels:["Jan","Feb","Mar","Apr"],
    datasets:[{label:"Sales",data:[120,200,150,80],backgroundColor:["#3b82f6","#06b6d4","#facc15","#ef4444"]}]
  },
  options:{
    responsive:true,
    plugins:{legend:{labels:{color:'#000'}}}
  }
});
