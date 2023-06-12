const express = require('express');
const multer = require('multer');
const { diskStorage } =require('multer');
const fs = require('fs');

const file = require('../models/file');

const router = express.Router();


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
router.post('/file/upload', (req, res, next) => {
  const upload = multer({
    storage: diskStorage({
      destination: (req, file, cb) => {
        cb(null, 'uploads/'); // Destination folder for uploaded files
      },
      filename: (req, file, cb) => {
        cb(null, file.originalname); // Use the original filename without appending the timestamp
      },
    }),
  }).single('file');

  upload(req, res, (err) => {
    // Handle multer upload middleware
    if (err instanceof multer.MulterError) {
      return res.status(400).json({ error: err.message });
    } else if (err) {
      return res.status(500).json({ error: 'Internal server error' });
    }

    // Continue with the rest of the route handler
    let id_user = '6462974d0a674ecf39e8320f';
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Access uploaded file properties
    const { filename, path: filePath, mimetype } = req.file;

    // Perform additional operations with the uploaded file
    const path_file = filePath;

    file.sendFileCloud(id_user, path_file, (err, cloud_data) => {
      if (err) {
        file.classifieFile(id_user, path_file, (err, classifieData) => {
          if (err) {
            const file_body = {
              name: filename,
              path: cloud_data.path,
              label: classifieData.label,
              language: classifieData.language,
              id_user: id_user,
            };
            file.createFile(file_body, (err, result) => {
              if (err) {
                deleteUploadedFile(path_file);
                res.redirect('/dashboard');
              } else {
                console.log(result);
                res.json(result);
              }
            });
          } else {
            res.json(classifieData);
          }
        });
      } else {
        res.json(cloud_data);
      }
    });
  });
});


// Function to delete the uploaded file
const deleteUploadedFile = (filePath) => {

  fs.unlink(filePath, (err) => {
    if (err) {
      console.error(`Failed to delete the file: ${err}`);
    } else {
      console.log('File deleted successfully');
    }
  });
};

const isAuth= (req,next)=>{
  let ses = req.session

  if(ses.id){
    
  }

}

router.get('/dashboard', (req, res) => {
  const id = '6462974d0a674ecf39e8320f';

  file.getLabel((err, data) => {
    let labels = [];
    if (err) {
      labels = data;
      file.getfiles(id, (err, files) => {
        const pack = {
          error: err ? false : true,
          message: err ? 'ok!' : files,
        };
        console.log(files)
        files.reverse();
        res.render('dashboard', { files: files, Err: pack, labels: labels });
      });
    }
  });
});



module.exports = router