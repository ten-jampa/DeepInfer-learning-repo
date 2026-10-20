/* Reusable inline-quiz widget. Usage:
   <div id="quiz" class="quiz"></div>
   <script src="../assets/quiz.js"></script>
   <script>
     window.QUIZ.render(document.getElementById("quiz"), [
       { q: "…", options: ["…","…","…"], correct: 0, explain: "…" }, …
     ]);
   </script>
   Feedback is instant; questions may be answered once (retake on reload = spacing practice). */
(function () {
  "use strict";

  function render(container, questions) {
    container.innerHTML = "";
    questions.forEach(function (item, qi) {
      var qEl = document.createElement("div");
      qEl.className = "q";
      qEl.id = "q" + (qi + 1);
      var qt = document.createElement("div");
      qt.className = "question";
      qt.textContent = (qi + 1) + ". " + item.q;
      qEl.appendChild(qt);

      // Shuffle option order so the answer isn't always first.
      var order = item.options.map(function (_, i) { return i; });
      for (var i = order.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var t = order[i]; order[i] = order[j]; order[j] = t;
      }
      var answered = false;
      order.forEach(function (oi) {
        var b = document.createElement("button");
        b.className = "option";
        b.textContent = item.options[oi];
        b.addEventListener("click", function () {
          if (answered) return;
          answered = true;
          var correctIdx = oi === item.correct;
          Array.prototype.forEach.call(qEl.querySelectorAll("button.option"), function (btn) {
            btn.disabled = true;
          });
          b.classList.add(correctIdx ? "correct" : "wrong");
          if (!correctIdx) {
            var rightBtn = qEl.querySelector('[data-oi="' + item.correct + '"]');
            if (rightBtn) rightBtn.classList.add("correct");
          }
          var v = document.createElement("p");
          v.className = "verdict " + (correctIdx ? "ok" : "bad");
          v.textContent = correctIdx ? "✓ Correct" : "✗ Not quite";
          qEl.appendChild(v);
          var ex = document.createElement("p");
          ex.className = "explain";
          ex.textContent = item.explain;
          qEl.appendChild(ex);
        });
        b.setAttribute("data-oi", oi);
        qEl.appendChild(b);
      });
      container.appendChild(qEl);
    });
  }

  window.QUIZ = { render: render };
})();
