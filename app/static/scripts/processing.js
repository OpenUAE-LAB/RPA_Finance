function gcaa_function(){
    setTimeout(async function(){
      try{
          fetch('/processing', {
              method: 'GET'
          }).then(function(response){
            if (response.ok){
                window.location.href='download';
            }
          })
      } catch (error){
          console.error(error);
      }
      }, 2000);
  }

gcaa_function();
