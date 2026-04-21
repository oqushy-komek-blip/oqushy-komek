const express = require('express');
const app = express();
app.use(express.static('public'));

app.get('/api/lang/:lang',(req,res)=>{
 if(req.params.lang==='kz'){
  res.json({title:"Оқушы платформасы"});
 } else {
  res.json({title:"Платформа ученика"});
 }
});

app.listen(3000,()=>console.log("http://localhost:3000"));