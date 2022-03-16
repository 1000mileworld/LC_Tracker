var tableData = []
for (const problem of my_problems) {
    tableData.push(problem)
}

//Define variables for input elements
var fieldEl = document.getElementById("filter-field");
var typeEl = document.getElementById("filter-type");
var valueEl = document.getElementById("filter-value");

//Trigger setFilter function with correct parameters
function updateFilter(){
    var filterVal = fieldEl.options[fieldEl.selectedIndex].value;
    var typeVal = typeEl.options[typeEl.selectedIndex].value;
    var filter = filterVal;
    if(filterVal){
        table.setFilter(filter,typeVal,valueEl.value);
    }
}

//Update filters on value change
document.getElementById("filter-field").addEventListener("change", updateFilter);
document.getElementById("filter-type").addEventListener("change", updateFilter);
document.getElementById("filter-value").addEventListener("keyup", updateFilter);

//Clear filters on "Clear Filters" button click
document.getElementById("filter-clear").addEventListener("click", function(){
    fieldEl.value = "title";
    typeEl.value = "like";
    valueEl.value = "";
    table.clearFilter();
});

//create Tabulator on DOM element
var table = new Tabulator("#problem-table", {
    height:465, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    
    initialSort:[
        {column:"last_solved", dir:"desc"}, //sort by this first
        //{column:"title", dir:"asc"}, //then sort by this second
    ],
    data:tableData, //assign data to table
    layout:"fitColumns", //fit columns to width of table (optional)
    columns:[ //Define Table Columns
    {title:"Number", field:"number"},    
    {title:"Title", field:"title"},
    {title:"Difficulty", field:"difficulty"},
    {title:"DS/Algo", field:"categories"},
    {title:"Self Rating", field:"rating"},
    {title:"Company", field:"companies"},
    {title:"Last Solved", field:"last_solved"},
    {title:"Next Solve", field:"next_solve"},

        // {title:"Age", field:"age", hozAlign:"left", formatter:"progress"},
        // {title:"Favourite Color", field:"col"},
        // {title:"Date Of Birth", field:"dob", sorter:"date"},
    ],
    pagination:true,
    //paginationSize:10,
});

table.on('rowClick', (e, row) => {
    location.href = `problem/${row.getData().id}/`;
})

//trigger download of data.csv file
document.getElementById("download-csv").addEventListener("click", function(){
    table.download("csv", "data.csv");
});