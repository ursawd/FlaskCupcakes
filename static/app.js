// APP.JS
// populate list of cupcakes
get_cupcakes();

// create list of cupcake sourced from db through flask api
async function get_cupcakes() {
    // get request to api for list of cupcakes
    const response = await axios.get("/api/cupcakes");
    // get number of cupcakes in list
    numCakes = response.data.cupcakes.length;
    // return single cupcake per iteration
    for (i = 0; i < numCakes; i++) {
        cCake = response.data.cupcakes[i];
        // append li with cupcake flavor to ol in index.html
        $("ol").append(`<li>${cCake.flavor}</li>`);
    }
    return;
}

$("#add-form").on("submit", async function (e) {
    e.preventDefault();
    // create js object of cupcake attribute values to use in post request
    let addData = {
        // values from form input id's
        flavor: $("#flavor").val(),
        size: $("#size").val(),
        rating: $("#rating").val(),
        image: $("#image").val(),
    };
    // send post request to flask api to add new cupcake to db
    const response = await axios.post("/api/cupcakes", addData);
    // clears input fields on form with name of add-form
    document.forms["add-form"].reset();
    // appends cupcake flavor to end of cupcake list
    $("ol").append(`<li>${addData["flavor"]}</li>`);
});
