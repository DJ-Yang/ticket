
function cardComponent (title, quantity, received, number) {

  let downloadButton;

  if (quantity < 1) {
    downloadButton = `<a href="#" class="btn btn-secondary disabled" role="button" aria-disabled=true tab-index=-1>이벤트 종료</a>`
  } else if (received == true) {
    downloadButton = `<a href="#" class="btn btn-secondary disabled" role="button" aria-disabled=true tab-index=-1>이용권 수령 완료</a>`
  } else {
    downloadButton = `<a href="#" class="btn btn-primary" data-number="${number}">이용권 받기</a>`
  }

  return `<div class="col" style="width: 16rem;">
      <img src="/static/img/novel-test-image.jpg" class="card-img-top">
      <div class="card-body">
        <h5 class="card-title">${title}<h5>
        ${downloadButton}
      </div>
    </div>
  `
}
