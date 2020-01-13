var openFile = function(file) {
    var input = file.target;
    console.log("Hi")

    var reader = new FileReader();
    reader.onload = function(){
      var dataURL = reader.result;
      var output = document.getElementById('profileunique');
      output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
  };