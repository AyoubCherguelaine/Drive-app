

async function logJSONData() {
    const response = await fetch("http://127.0.0.1:8000/file/fileinfo/"+fileId);
    const jsonData = await response.json();
    console.log(jsonData);
}


async function showFileInfo(fileId) {
    // Use the fileId parameter as needed
    const fileInfoContent = document.getElementById('fileInfoContent');
    fileInfoContent.innerHTML= ""
    let url ='http://127.0.0.1:8000/file/fileinfo/'+fileId
    console.log(url)
    fetch(url, {
        method: 'GET',
        headers: {
          'accept': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          // Handle the response data here
          console.log(data);
          const creatorUser = data.users[0];
      const otherUsers = data.users.slice(1); // Get all users except the first one
      
      // Update the file info in the HTML
      const fileInfoContent = document.getElementById('fileInfoContent');
      fileInfoContent.innerHTML = `
        <p><strong>File ID:</strong> ${data.file._id}</p>
        <p><strong>File Name:</strong> ${data.file.name}</p>
    
        <p><strong>File Label:</strong> ${data.file.label}</p>
        <p><strong>File Language:</strong> ${data.file.language}</p>
        <p><strong>Creator User ID:</strong> ${creatorUser._id}</p>
        <p><strong>Creator User Name:</strong> ${creatorUser.name}</p>
        <p><strong>Other Users:</strong></p>
        <ul>
          ${otherUsers.map(user => `<li>${user.name}</li>`).join('')}
        </ul>
        <
      `;
        })
        .catch(error => {
          // Handle any errors here
          console.error(error);
        });
  }