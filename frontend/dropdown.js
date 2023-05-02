function chooseState(state) {
    let selected = state.options[state.selectedIndex].innerHTML;
    let value = state.value;
    alert("Selected state: " + selected + ". Value: " + value);
}
