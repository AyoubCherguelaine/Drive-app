const express = require('express');
const file = require("../models/file")
const router = express.Router();

const multer = require('multer');
const path = require('path');
const fs = require('fs');


// Set up multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/'); // Destination folder for uploaded files
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname); // Use the original filename without appending the timestamp
  },
});

// Set up multer upload instance
const upload = multer({ storage });

// Use the upload middleware in your route handler
router.post('/file/upload', upload.single('file'), (req, res) => {

  let id_user = "6462974d0a674ecf39e8320f"
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Access uploaded file properties
  const { filename, path: filePath, mimetype } = req.file;

  // Perform additional operations with the uploaded file
  path_file = filePath

  file.sendFileCloud(id_user,path_file,(err,cloud_data)=>{
    if(err){
// Send a response with the uploaded file details
    
      
    file.classifieFile(id_user,path_file,(err,classifieData)=>{
      if(err){
        res.send({"cloud":cloud_data,"classifer":classifieData})
        file_body = {
          name : "filename",
          path : cloud_data.dr_path+"/"+ cloud_data.filename,
          label : classifieData.label,
          language :classifieData.language,
          id_user :id_user
        }
        file.createFile(file_body,(err,result)=>{
          if(err){
            deleteUploadedFile(path_file)
            res.redirect("/dashboad")
          }else{
            console.log(result)
            res.json(result)
          }
        })
      }else{
        res.json(classifieData)
      }
    })

    }else{
      res.json(cloud_data)
    }
  })

  
});

// Function to delete the uploaded file
function deleteUploadedFile(filePath) {
  fs.unlink(filePath, (err) => {
    if (err) {
      console.error(`Failed to delete the file: ${err}`);
    } else {
      console.log('File deleted successfully');
    }
  });
}



router.get("/dashboard", (req, res) => {
  const id = "6462974d0a674ecf39e8320f";

  file.getLabel((err,data)=>{
    labels = []
    let pack;
    if(err){
      labels= data
      file.getfiles(id, (err, files) => {
    
      
        if (err) {
          
          pack = {
            error: false,
            message: "ok!",
          };
        } else {
          pack = {
            error: true,
            message: files,
          };
          files = []; // Reset files to an empty array
        }
        
        res.render("dashboard", { files, Err: pack,labels:labels });
      });
    }else{

      //console.log(data)
    }
  })
  
});


module.exports = router