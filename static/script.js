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
				console.log("Something went wrong!")
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
				console.log("Something went wrong!")
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
				console.log("Something went wrong!")
				console.log(error)
      }

    });
}

function removeButtonClicked(user_id, photo_id) {
    console.log("Remove button clicked");
    $.ajax({
        url: '/remove',
        data: {"user_id": user_id, "photo_id" : photo_id},

    success: function(response) {
        console.log(response)
        console.log("1")
        location.reload();

      },
      error: function(error) {
				console.log("Something went wrong!")
				console.log(error)
      }

    });
}

function removeFavouriteButtonClicked(user_id, photo_id) {
    console.log("Remove button clicked");
    $.ajax({
        url: '/removefavourite',
        data: {"user_id": user_id, "photo_id" : photo_id},

    success: function(response) {
        console.log(response)
        console.log("1")
        location.reload();

      },
      error: function(error) {
				console.log("Something went wrong!")
				console.log(error)
      }

    });
}

function favouriteButtonClicked(user_id, photo_id) {
    console.log("Favourite button clicked");
    $.ajax({
        url: '/addfavourite',
        data: {"user_id": user_id, "photo_id" : photo_id},

    success: function(response) {
        console.log(response)
        console.log("1")
        location.reload();

      },
      error: function(error) {
				console.log("Something went wrong!")
				console.log(error)
      }

    });
}

function getDiscription() {
    var userInput = document.getElementById('userInput').value;
    console.log(userInput);
    $.ajax({
        url: '/upload',
        data: {"userInput": userInput},

    success: function(response) {
        console.log(response)
        console.log("succes")

      },
      error: function(error) {
				console.log("Something went wrong!")
				console.log(error)
      }
    });
}

function removeProfilePicButtonClicked() {
    console.log("Remove button clicked");
    $.ajax({
        url: '/removeprofilepicture',

    success: function(response) {
        console.log(response)
        console.log("1")
        location.reload();

      },
      error: function(error) {
				console.log("Something went wrong!")
				console.log(error)
      }

    });
}