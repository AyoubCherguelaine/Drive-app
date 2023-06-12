const express = require('express');

const router = express.Router();

const authModel = require("../models/Auth")


router.get("/login",(req,res)=>{
    let pack = {
      error:false,
      message:"ok !"
    }
  
    res.render("login",{pack:pack})
  })

router.get("/login/error",(req,res)=>{
    const { error, message } = req.query;
        
    let pack = {
        error:Boolean(error),
        message:message
      }
      console.log(req.query)
    res.render("login",{pack:pack})
})

router.post("/login",(req,res)=>{
    const { email, password } = req.body;
    console.log(req.body)
  // Perform data validation
    if (!email || !password) {
        let error = true;
        let message = 'Data not valid!';
        
        res.redirect(`/login/error?error=${error}&message=${message}`)
    }else{

        authModel.login(req.body,(err,data)=>{
            if(!err){
                let error = true;
                let message = 'api problem contact admin';
                res.redirect(`/login/error?error=${error}&message=${message}`)
            }else{
                //{"state":False}
                let {stat} = data
               
                if(stat){
                    // auth

                    let id= data["_id"]
                   let name = data["name"]

                    req.session.id = id;
                    req.session.name = name
                    res.redirect("/dashboad")
                   
                }else{
                    // not auth
                    let error = true;
                    let message = 'You have a problem with your email or password.';
                    res.redirect(`/login/error?error=${error}&message=${message}`)
                   
                }

            }
        })

    }

})
  
router.get("/signup",(req,res)=>{
    let pack = {
      error:false,
      message:"ok !"
    }
    res.render("signup",{pack:pack})
})

router.get("/signup/error",(req,res)=>{
    const { error, message } = req.query;
  
    let pack = {
        error:Boolean(error),
        message:message
      }

    res.render("signup",{pack:pack})
})

router.post("/signup",(req,res)=>{
    let  {name,password,email} = req.body
    console.log(req.body)

    if (!name || !email || !password) {
        let error = true;
        let message = 'Data not valid!';
        res.redirect(`/signup/error?error=${error}&message=${message}`)
    }else{

        authModel.createUser(req.body,(err,result)=>{
            if(err){
                /*
                "_id"
                "name":self.name,
            "email":self.email,
            "password":self.password,
            "files":self.files
                */
               let email= result.email
               let password= result.password
               let id= result["_id"]
                let name = result["name"]

                req.session.id = id;
                req.session.name = name
                res.redirect("/dashboad")
                
            }else{
                let error = true;
                let message =  result;
                res.redirect(`/signup/error?error=${error}&message=${message}`)
            }
        })
    }
    
})

module.exports = router;
