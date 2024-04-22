// Lấy ra tất cả các thẻ oembed trong nội dung
const oembeds = document.querySelectorAll('oembed');

// Duyệt qua từng thẻ oembed và thực hiện việc chuyển đổi
oembeds.forEach(oembed => {
    // Lấy URL của video từ thuộc tính url của thẻ oembed
    const url = oembed.getAttribute('url');
    // Tạo một thẻ iframe
    const iframe = document.createElement('iframe');
    // Thiết lập thuộc tính src của iframe để nhúng video từ URL
    iframe.src = 'https://www.youtube.com/embed/' + getVideoId(url);
    // Thiết lập các thuộc tính khác của iframe theo ý muốn
    iframe.width = '560';
    iframe.height = '315';
    iframe.allowFullscreen = true;
    iframe.frameborder = '0';
    // Thay thế thẻ oembed bằng thẻ iframe
    oembed.parentNode.replaceChild(iframe, oembed);
});

// Hàm để lấy ID của video từ URL YouTube
function getVideoId(url) {
    // Regex để lấy ID của video từ URL
    const regex = /[?&]([^=#]+)=([^&#]*)/g;
    let match;
    while (match = regex.exec(url)) {
        if (match[1] === 'v') {
            return match[2];
        }
    }
    return null;
}
