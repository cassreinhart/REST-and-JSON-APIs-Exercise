const BASE_URL = 'http://localhost:5000/api/cupcakes'
const $cupcakesList = $('.cupcakes ul');
const $addCupcakeForm = $('#new-cupcake');

async function getCupcakeData() {
    //make request to API to get JSON of all cupcakes
    let resp = await axios.get(BASE_URL);
    let cupcakes = resp.data.cupcakes;
    return putCupcakesOnPage(cupcakes);
}

function cupcakeMarkup(cupcake) {
    //insert html string to dynamically put in UL
    return `
        <div data-cupcake-id="${cupcake.name}">
            <li>
                ${cupcake.name} | ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
                <button class="delete"> Remove </button>
                <button class="edit"> Edit </button>
            </li>
            <img class="cupcake-image"
                src="${cupcake.image}">
        </div>
    `;
}

function putCupcakesOnPage(cupcakes) {
    // manipulate DOM to add cupcakes to UI
    for (let cupcake of cupcakes) {
        let newCupcake = $(cupcakeMarkup(cupcake));
        $cupcakesList.append(newCupcake);
    }
}

async function handleNewCupcakeForm(e) {
    // make post request to API to submit new JSON for new cupcake
    let flavor = $('#flavor').val();
    let size = $('#size').val()
    let rating = $('#rating').val()
    let image = $('#image').val()

    const resp = await axios.post(BASE_URL, 
        {
            flavor, 
            size,
            rating,
            image
        });

    let newCupcake = $(cupcakeMarkup(resp.data.cupcake));
    $cupcakesList.append(newCupcake);
    $addCupcakeForm.trigger("reset");
}

$addCupcakeForm.on("submit", handleNewCupcakeForm(e))

$cupcakesList.on('click', '.delete', async function(e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest('div');
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/${cupcakeId}`);
    $cupcake.remove();
});

getCupcakeData();