const http = require('http');
const socketIO = require('socket.io');
const fs = require('fs');



    // Handle 'file-upload' event from the client
const UploadFile  = (file) => {
      const { filename, data } = file;
        console.log("click")
      // Save the file on the server
      fs.writeFile(`uploads/${filename}`, data, (err) => {
        if (err) {
          console.error(`Failed to save the file: ${err}`);
          socket.emit('file-upload-error', { error: 'Failed to save the file' });
        } else {
          console.log('File saved successfully');
          socket.emit('file-upload-success', { message: 'File uploaded successfully' });
        }
      });
    }
  

module.exports = {
    UploadFile
}