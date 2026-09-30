function showPlanner(name) {
  document.querySelectorAll('.planner-panel').forEach(x => {
    x.classList.remove('active');
  });

  const panel = document.getElementById(name + '-panel');

  if (panel) {
    panel.classList.add('active');
    panel.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
}


function formObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}


async function sendJSON(url, data) {

  const loading = document.getElementById('loading');

  try {

    if (loading) {
      loading.classList.remove('hidden');
    }

    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });


    const text = await res.text();

    let out;

    try {
      out = JSON.parse(text);
    } catch (error) {
      console.error('Invalid server response:', text);
      throw new Error('Server returned an invalid response.');
    }


    if (!res.ok) {
      throw new Error(
        out.message || 'Request failed'
      );
    }


    renderResults(
      out.result || {},
      out.category || 'home'
    );

  } catch (err) {

    console.error('API Error:', err);

    alert(
      'Error: ' + (err.message || 'Something went wrong')
    );

  } finally {

    if (loading) {
      loading.classList.add('hidden');
    }

  }
}


async function submitHome(e) {

  e.preventDefault();

  try {

    const data = formObject(e.target);

    await sendJSON(
      '/generate-home',
      data
    );

  } catch (err) {

    console.error(err);

  }
}


async function submitParty(e) {

  e.preventDefault();

  try {

    const data = formObject(e.target);

    await sendJSON(
      '/generate-party',
      data
    );

  } catch (err) {

    console.error(err);

  }
}


async function submitJewelry(e) {

  e.preventDefault();

  const loading = document.getElementById('loading');

  try {

    if (loading) {
      loading.classList.remove('hidden');
    }


    const formData = new FormData(e.target);

    const res = await fetch(
      '/generate-jewelry',
      {
        method: 'POST',
        body: formData
      }
    );


    const text = await res.text();

    let out;

    try {
      out = JSON.parse(text);
    } catch (error) {
      console.error('Invalid server response:', text);
      throw new Error('Server returned an invalid response.');
    }


    if (!res.ok) {

      throw new Error(
        out.message || 'Request failed'
      );

    }


    renderResults(
      out.result || {},
      out.category || 'jewelry'
    );


  } catch (err) {

    console.error('Jewelry API Error:', err);

    alert(
      'Error: ' + (err.message || 'Something went wrong')
    );


  } finally {

    if (loading) {
      loading.classList.add('hidden');
    }

  }
}


function money(n) {

  return '₹' +
    Number(n || 0).toLocaleString('en-IN');

}


function renderResults(result, category) {

  const el = document.getElementById('results');

  if (!el) {
    console.error('Results element not found.');
    return;
  }


  const recommendations =
    Array.isArray(result.recommendations)
      ? result.recommendations
      : [];


  const recs = recommendations.map(r => `

    <div class="recommendation">

      <h4>
        ${escapeHtml(
          r.name || 'Recommendation'
        )}
      </h4>

      <div>
        ${escapeHtml(
          r.platform || 'Platform'
        )}
      </div>

      <p>
        ${escapeHtml(
          r.reason || 'Budget-friendly option'
        )}
      </p>

      <div class="price">
        ${money(r.estimated_price)}
      </div>

      ${
        r.link
          ? `
            <a
              href="${escapeHtml(r.link)}"
              target="_blank"
              rel="noopener"
            >
              View platform
            </a>
          `
          : ''
      }

    </div>

  `).join('');


  const budgetBreakdown =
    Array.isArray(result.budget_breakdown)
      ? result.budget_breakdown
      : [];


  const breakdown =
    budgetBreakdown.map(x => `

      <li>
        ${escapeHtml(x.category || 'Category')}:
        <b>
          ${money(x.amount)}
        </b>
      </li>

    `).join('');


  const tipsArray =
    Array.isArray(result.tips)
      ? result.tips
      : [];


  const tips =
    tipsArray.map(x => `

      <li>
        ${escapeHtml(x)}
      </li>

    `).join('');


  const categoryName =
    String(category || 'home');


  el.innerHTML = `

    <div class="result">

      <h2>
        ✨
        ${
          categoryName.charAt(0).toUpperCase()
          + categoryName.slice(1)
        }
        Recommendations
      </h2>


      <p>
        ${escapeHtml(
          result.summary ||
          'Your personalized plan is ready.'
        )}
      </p>


      <h3>
        Budget Breakdown
      </h3>

      <ul>
        ${breakdown}
      </ul>


      <h3>
        Recommendations
      </h3>

      <div class="cards">
        ${recs}
      </div>


      <h3>
        Smart Tips
      </h3>

      <ul>
        ${tips}
      </ul>


      <small>
        Mode:
        ${escapeHtml(
          result.mode || 'demo'
        )}
      </small>

    </div>

  `;


  el.scrollIntoView({
    behavior: 'smooth'
  });

}


function escapeHtml(value) {

  return String(value ?? '').replace(
    /[&<>"']/g,
    function (m) {

      return {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'

      }[m];

    }
  );

}


async function auth(e, type) {

  e.preventDefault();

  try {

    const emailElement =
      document.getElementById('email');

    const passwordElement =
      document.getElementById('password');

    const data = {

      email: emailElement
        ? emailElement.value
        : '',

      password: passwordElement
        ? passwordElement.value
        : ''

    };


    if (type === 'register') {

      const nameElement =
        document.getElementById('name');

      data.name = nameElement
        ? nameElement.value
        : '';

    }


    const res = await fetch(
      '/' + type,
      {
        method: 'POST',

        headers: {
          'Content-Type':
            'application/json'
        },

        body: JSON.stringify(data)
      }
    );


    const text = await res.text();

    let out;

    try {

      out = JSON.parse(text);

    } catch (error) {

      console.error(
        'Invalid authentication response:',
        text
      );

      throw new Error(
        'Server returned an invalid response.'
      );

    }


    const message =
      document.getElementById(
        'auth-message'
      );


    if (message) {

      message.textContent =
        out.message || '';

    }


    if (out.ok && out.redirect) {

      location.href =
        out.redirect;

    }


  } catch (err) {

    console.error(
      'Authentication error:',
      err
    );


    const message =
      document.getElementById(
        'auth-message'
      );


    if (message) {

      message.textContent =
        err.message ||
        'Something went wrong.';

    }

  }

}