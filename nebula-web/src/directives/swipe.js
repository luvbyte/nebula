export const vSwipe = {
  mounted(el, binding) {
    let startX = 0;
    let startY = 0;
    const threshold = binding.arg || 40;

    el.addEventListener("touchstart", e => {
      // Prevent parent swipe from seeing this touch
      e.stopPropagation();

      startX = e.changedTouches[0].clientX;
      startY = e.changedTouches[0].clientY;
    }, { passive: true });

    el.addEventListener("touchend", e => {
      // Prevent parent swipe from firing
      e.stopPropagation();

      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;

      const deltaX = endX - startX;
      const deltaY = endY - startY;

      let direction = null;

      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (Math.abs(deltaX) > threshold) {
          direction = deltaX > 0 ? "right" : "left";
        }
      } else {
        if (Math.abs(deltaY) > threshold) {
          direction = deltaY > 0 ? "down" : "up";
        }
      }

      if (direction && typeof binding.value === "function") {
        binding.value(direction);
      }
    }, { passive: true });
  }
};

// no use for now
export const vSwipeStop = {
  mounted(el) {
    el.setAttribute("data-swipe-stop", "");
  }
};