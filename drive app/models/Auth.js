const axios = require('axios');
const {ModelApi,ClassifierApi,CloudApi} = require("./config")


const createUser = async (body,callback) => {
    try {
        const { name, email, password } = body;
        if(!name || !email || !password){
          console.log('Missing data fields');
            callback(false,'Missing data fields' );
        }else{

            const userData = body;
            isNewUser(body, async (err,result)=>{
              if(err) callback(false,err)
              if(result){
                  let url ='/user/create'
                  console.log('send');
                  ModelApi.post(url,userData).then((res)=>{
                    callback(true,res)
                  }).catch((err)=>{
                    callback(fasle,err)
                  })
                  
              }
            })
        }

    } catch (error) {
      console.error('Error creating user:', error);
      callback(false,error);
    }
  }

const isNewUser = async (body,callback) => {
    try {
        let {email} = body
        if ( ! email){
            callback(fasle,{error:'Missing data fields' })
        }
      const userData = body;
        let url ='/user/isnewuser'
        const json = JSON.stringify(userData);
      ModelApi.post(url,json).then((res)=>{
        callback(true,res)
      }).catch((err)=>{
        callback(fasle,err)
      })
      

    } catch (error) {
      console.error('Error checking if user is new:', error);
        callback(error,null);   
     }
  }

const login =  async (body,callback) => {
    try {

        let {email,password} = body
        
        if( !email || !password){
            callback(false,{error:'Missing data fields' })
        }else{

            const userData = body;
            let url ='/user/login'
            
             ModelApi.post(url,userData).then((res)=>{
              
               callback(true,res.data)

             }).catch((err)=>{
               callback(false,err)
             })

        }

    } catch (error) {
      console.error('Error logging in:', error);
      callback(fasle ,error);
    }
  }

// 6462974d0a674ecf39e8320f 646299ce6145d673d8b4046f
const isAllowFile = async (id_user, id_file, callback) => {
    try {

      // Check if the user has permission to access the file
    // Make a request to the API endpoint

            let url = `/file/isFileAllow/${id_user}/${id_file}`
             ModelApi.get(url).then((res)=>{
              const isAllowed = res.data; // Replace with your actual permission check logic
  
               if (isAllowed) {
                  callback(null, { allowed: true });
                } else {
                  callback(null, { allowed: false });
                }
              
             }).catch((err)=>{
               callback(fasle,err)
             })

    } catch (error) {
      callback({ error: 'An error occurred' }, null);
    }
  }


const getUser = async (id_user,callback)=>{
  // /user/{id}

    let url ='/user/'+id_user
             ModelApi.get(url).then((res)=>{
               callback(true,res)
             }).catch((err)=>{
               callback(fasle,err)
             })

}

const getUsers = async (ids,callback)=>{
  const response = await axios.post(modelManager+'/user/ids',ids);


  let url ='/user/'+id_user
             ModelApi.get(url).then((res)=>{
              const {data} = res
              if(data){
                callback(true,data)
              }else{
                callback(false,null)
              }

             }).catch((err)=>{
               callback(fasle,err)
             })
}

module.exports = {
    createUser,
    login,
    isAllowFile,
    getUser,
    getUsers
}