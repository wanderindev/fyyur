window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.addEventListener("DOMContentLoaded", () => {
  const deleteBtn = document.getElementById('delete-btn');
  if (deleteBtn) {
    deleteBtn.onclick = e => {
    const delId = e.target.dataset.id;
    fetch('/venues/' + delId, {
      method: 'DELETE'
    })
        .then(() => {

        })
    }
  }
});
