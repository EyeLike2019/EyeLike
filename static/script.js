// like, skip and dislike button-actions
function likeButtonClicked(photo_id) {
    console.log("Like button clicked")
    $.ajax({
        url: '/updatescore',
		data: {"newscore": "1", "photo_id" : photo_id},

      success: function(response) {

        console.log(response)
	    console.log("1")

	   location.reload();

      },
      error: function(error) {
				console.log("Er ging iets mis!")
				console.log(error)
      }
    });

}

function skipButtonClicked(photo_id) {
    console.log("Skip button clicked")
    $.ajax({
        url: '/updatescore',
	    data: {"newscore": "0", "photo_id": photo_id},

	  success: function(response) {

        console.log(response)
	    console.log("1")

	    location.reload();

      },
      error: function(error) {
				console.log("Er ging iets mis!")
				console.log(error)
      }
    });
}

function dislikeButtonClicked(photo_id) {
    console.log("Skip button clicked")
    $.ajax({
        url: '/updatescore',
		data: {"newscore": "-1", "photo_id": photo_id},
	success: function(response) {

        console.log(response)
	    console.log("1")
	    location.reload();

      },
      error: function(error) {
				console.log("Er ging iets mis!")
				console.log(error)
      }

    });
}

$.getJSON(
    "https://api.unsplash.com/photos/random/?query=fashion&client_id=8f5cd8cd9e1c27d5b5c6d283c243726afcf1a7ad7602c1ee0f6a0702f5272a0f",
    function(data) {
        var pic = data.links.html

    $(".api").attr("src", pic)
    });