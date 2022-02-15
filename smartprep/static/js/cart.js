var updateBtns = document.getElementsByClassName('update-cart')


for(var i=0; i<updateBtns.length; i++){
   updateBtns[i].addEventListener('click',function(){
      var iId= this.dataset.i
      var action= this.dataset.action
      console.log ('iId:',iId,'action:',action)

      console.log('USER:',user)
      if(user=== 'AnonymousUser'){
          console.log('Not logged in')
      }
      else{

        updateUserOrder(iId,action)
      }
   })
}

function updateUserOrder(iId,action){
     console.log('User is logged in,sending data....')

     var url='/materials/update_item/'

     fetch(url,{
          method:'POST',
          headers:{
              'Content-Type':'application/json',
              'X-CSRFToken':csrftoken,
          },
          body:JSON.stringify({'iId':iId,'action':action})

     })

     .then((response)=>{
        return response.json()

     })
     .then((data)=>{
        console.log('data:',data)
        location.reload()

     })




}