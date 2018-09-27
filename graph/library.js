party_colour = type => {
  switch(type) {
    case 'National': return 'blue';
    case 'Labour': return 'red';
    case 'NZ First': return 'black';
    case 'Green': return 'green';
    case 'ACT': return 'yellow';
    default: return '#888';
  }
}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}
