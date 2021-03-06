/* like button */
function likeButtonClicked(photo_id) {
    console.log("Like button clicked");
    $.ajax({
        url: '/updatescore',
        data: {
            "newscore": "1",
            "photo_id": photo_id
        },

        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* skip button */
function skipButtonClicked(photo_id) {
    console.log("Skip button clicked");
    $.ajax({
        url: '/updatescore',
        data: {
            "newscore": "0",
            "photo_id": photo_id
        },

        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* dislike button */
function dislikeButtonClicked(photo_id) {
    console.log("Skip button clicked");
    $.ajax({
        url: '/updatescore',
        data: {
            "newscore": "-1",
            "photo_id": photo_id
        },
        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* remove button */
function removeButtonClicked(user_id, photo_id) {
    console.log("Remove button clicked");
    $.ajax({
        url: '/remove',
        data: {
            "user_id": user_id,
            "photo_id": photo_id
        },

        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* remove-profile picture button */
function removeProfilePicButtonClicked(profile_pic) {
    console.log("Remove button clicked");
    $.ajax({
        url: '/removeprofilepicture',
        data: {
            "profile_pic": profile_pic
        },

        success: function(response) {

            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!")
            console.log(error)
        }

    });
}

/* remove-favourite button */
function removeFavouriteButtonClicked(user_id, photo_id) {
    console.log("Remove button clicked");
    $.ajax({
        url: '/removefavourite',
        data: {
            "user_id": user_id,
            "photo_id": photo_id
        },

        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* add-to-favourite button */
function favouriteButtonClicked(user_id, photo_id) {
    console.log("Favourite button clicked");

    /* check if post is already in favourites */
    var alert = document.getElementById("succes-favorite-alert");
    var alert2 = document.getElementById("fail-favorite-alert");

    $.ajax({
        url: '/addfavourite',
        data: {
            "user_id": user_id,
            "photo_id": photo_id
        },

        success: function(response) {

            /* show the correct type of alert and let it disappear after 3 seconds*/
            if (response == "Succes") {
                alert.style.display = "block";
                setTimeout(function() {
                    document.getElementById("succes-favorite-alert").style.display = "none";
                }, 3000);
            } else {
                alert2.style.display = "block";
                setTimeout(function() {
                    document.getElementById("fail-favorite-alert").style.display = "none";
                }, 3000);
            }

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* load-more button */
function load_more(template) {
    console.log("Load more button clicked");
    $.ajax({
        url: '/load_more',
        data: {
            "template" : template
        },

        success: function(response) {
            location.reload();

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}

/* autocomplete function search bar */
function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;

    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();

        if (!val) {
            return false;
        }
        currentFocus = -1;

        /*if user doesn't type @, add it to the input value*/
        if (val[0] != "@") {
            val = "@" + val
        }

        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);

        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase() && val.length > 1) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");

                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);

                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {

                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    searchFunction();

                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");

        if (x) x = x.getElementsByTagName("div");

        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable and make the
            current item more visible:*/
            currentFocus++;
            addActive(x);

        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable and make the
            current item more visible:*/
            currentFocus--;
            addActive(x);

        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, submit the current item*/
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
            searchFunction();
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}

/* search user */
function searchFunction() {
    var nameValue = document.getElementById("searchbar").value;
    if (nameValue) {
        window.location = '/search/' + nameValue;
    }
}

/* follow button */
function followButtonClicked(user_id, follower_id) {
    console.log("Follow button clicked");
    var button = document.getElementById("follow");

    $.ajax({
        url: '/already_following',
        data: {
            "user_id": user_id,
            "follower_id": follower_id
        },

        success: function(response) {
            console.log(response);

            /* if user doesn't follow concerned user, call follow-function */
            if (response == "False") {
                $.ajax({
                    url: '/follow',
                    data: {
                        "user_id": user_id,
                        "follower_id": follower_id
                    },

                    success: function(response) {

                        /* change button style after user has followed concerned user */
                        button.style.background = 'green';
                        button.innerHTML = '<b>Following</b>';
                        location.reload();

                    },
                    error: function(error) {
                        console.log("Something went wrong!");
                        console.log(error);
                    }

                });

            /* if user already follows concerned user, call unfollow-function */
            } else {
                $.ajax({
                    url: '/unfollow',
                    data: {
                        "user_id": user_id,
                        "follower_id": follower_id
                    },

                    success: function(response) {

                        /* change button style after user has unfollowed concerned user */
                        button.style.background = 'black';
                        button.innerHTML = '<b>Follow</b>';
                        location.reload();

                    },
                    error: function(error) {
                        console.log("Something went wrong!");
                        console.log(error);
                    }

                });
            }

        },
        error: function(error) {
            console.log("Something went wrong!");
            console.log(error);
        }

    });
}