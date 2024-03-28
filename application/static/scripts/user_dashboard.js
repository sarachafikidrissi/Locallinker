let availableKeywords = [
    'Home Cleaning',
    'Plumbing',
    'Event Planning',
    'Assembly',
    'Electrical',
    'General Handyman',
];

const resultBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box")

inputBox.onkeyup = function(){
    let result = []; //will store all filtered keyword that we have in availableKeywords array
    let input = inputBox.value; //will store value available in this inputBox
    if(input.length){
        result = availableKeywords.filter((keyword)=>{
            return keyword.toLowerCase().includes(input.toLowerCase()); //this line checks if the keyword string (converted to lowercase) contains the input string (also converted to lowercase)

        }); 
        console.log(result);
    }
    display(result);

    if(!result.length){
        resultBox.innerHTML = ''; // it removes the horizental line that appears if the input doesn't exist 
    }
}//will store filtered data in this result

//Display result
function display(result){
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this)>" + list + "<li>";
    });

    resultBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    inputBox.value = list.innerHTML; //to show the selected input in the search box
    resultBox.innerHTML = ''; //to hide everything after selecting
}

function submitFormOrNext() {
    // Check if the current tab is the last one
    if (currentTab == (tab.length - 1)) {
        document.getElementById("regForm").submit(); // Submit the form
    } else {
        nextPrev(1); // Go to the next tab
    }
}