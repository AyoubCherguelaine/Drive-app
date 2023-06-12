const axios = require('axios');
const { ModelApi, ClassifierApi, CloudApi } = require('./config');
const auth = require('./Auth');
const FormData = require('form-data');
const fs = require('fs');


class file{
    constructor(name, path, label, language, id_user) {
        this.name = name;
        this.path = path;
        this.label = label;
        this.language = language;
        this.id_user = id_user;
      }

      async save(callback) {
        if (!this.name || !this.path || !this.label || !this.language || !this.id_user) {
          callback(false, 'Missing Data');
        } else {
          const fileData = {
            name: this.name,
            path: this.path,
            label: this.label,
            language: this.language,
            id_user: this.id_user,
          };
          const url = '/file/create';
      
          try {
            const res = await ModelApi.post(url, fileData);
            callback(true, res.data);
          } catch (err) {
            callback(false, err);
          }
        }
      }
      
      static async delete(id_file, callback) {
        if (!id_file) {
          callback(false, 'Missing Data');
        } else {
          const url = `/file/${id_file}/delete`;
      
          try {
            const res = await ModelApi.get(url);
            const { data } = res;
            if (data.result === true) {
              callback(true, null);
            } else {
              callback(false, 'API operation');
            }
          } catch (err) {
            callback(false, err);
          }
        }
      }
      

    static share(id_file,id_user, callback){
      if(! id_file || ! id_user){
        callback(false,null)
      }else{
        let url = `/user/${id_user}/share/${id_file}`
        ModelApi.get(url).then((res)=>{
          callback(true,null)
        }).catch((err)=>{

          callback(false,err)
        })
      }
    }
}
const createFile = async (body, callback) => {
  const { name, path, label, language, id_user } = body;
  if (name && path && label && language && id_user) {
    const newFile = new file(name, path, label, language, id_user);
    newFile.save(async (err, result) => {
      if (err) {
        file.share(result['_id'], id_user, (err, r) => {
          if (err) {
            callback(true, result);
          }
        });
      } else {
        callback(false, result);
      }
    });
  } else {
    callback(false, 'Missing Data');
  }
};


const deleteFile = async (id_file,callback)=>{

    file.delete(id_file,callback);

}

const fileInfo = async (id_user,id_file,callback)=>{

    auth.isAllowFile(id_user,id_file,async (err,result)=>{
        if(err) callback(false,err)
        else{
            if(result.allowed){

            
        
            let url= '/file/fileinfo/'+id_file

            ModelApi.get(url).then((res)=>{

                callback(true,res.data)

              }).catch((err)=>{

                callback(fasle,err)
              })
            }else{
                callback(false,"not Allowed")
            }
        }
    })


}

const getfiles = async (id_user,callback)=>{

    let urlu = "/user/"+id_user
    ModelApi.get(urlu).then((res)=>{
        user = res.data
        files = user.files
        
        let url = '/file/ids'
        let body = {
            "ids":  files
          }
          const jsonString = JSON.stringify(body);
        console.log(jsonString);
        
          
        ModelApi.post(url,body).then((res)=>{
          
            callback(true,res.data)
            
           }).catch((err)=>{

             
             callback(false,null)
              
           })

      }).catch((err)=>{

        callback(false,err)
      })

    
}

const getLabel = async (callback)=>{

    let url = "/labels"

    ClassifierApi.get(url).then((res)=>{
          
        callback(true,res.data)

       }).catch((err)=>{

         callback(false,err)
       })

}
const sendFileCloud = async (id, filePath, callback) => {
  const url = `/upload/${id}`;

  try {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));

    const res = await CloudApi.post(url, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...form.getHeaders(),
      },
    });
    callback(true, res.data);
  } catch (err) {
    callback(false, err);
  }
};

const classifieFile = async (id, filePath, callback) => {
  const url = `/classify`;

  try {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));

    const res = await ClassifierApi.post(url, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...form.getHeaders(),
      },
    });
    callback(true, res.data);
  } catch (err) {
    callback(false, err);
  }
};






module.exports = {
    fileInfo,
    deleteFile,
    createFile,
    getfiles,
    getLabel,
    sendFileCloud,
    classifieFile
}