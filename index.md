---
layout: default
title: DevSecOps-22
---

{% assign linux_lessons       = site.pages | where_exp: "p", "p.url contains '/linux/lessons/'" | sort: "url" %}
{% assign linux_labs          = site.pages | where_exp: "p", "p.url contains '/linux/labs/'" | sort: "url" %}
{% assign linux_cheatsheets   = site.pages | where_exp: "p", "p.url contains '/linux/cheatsheets/'" | sort: "url" %}
{% assign linux_pdfs          = site.static_files | where_exp: "f", "f.path contains '/linux/pdf/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}
{% assign linux_cheat_pdfs    = site.static_files | where_exp: "f", "f.path contains '/linux/cheatsheets/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}

{% assign python_lessons      = site.pages | where_exp: "p", "p.url contains '/python/lessons/'" | sort: "url" %}
{% assign python_labs         = site.pages | where_exp: "p", "p.url contains '/python/labs/'" | sort: "url" %}
{% assign python_cheat_pdfs   = site.static_files | where_exp: "f", "f.path contains '/python/cheatsheets/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}
{% assign python_pdfs         = site.static_files | where_exp: "f", "f.path contains '/python/pdf/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}
{% assign python_classcode    = site.static_files | where_exp: "f", "f.path contains '/python/classcode/'" | where_exp: "f", "f.extname == '.py'" | sort: "path" %}

{% assign git_lessons         = site.pages | where_exp: "p", "p.url contains '/GIT/lessons/'" | sort: "url" %}
{% assign git_pdfs            = site.static_files | where_exp: "f", "f.path contains '/GIT/PDF/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}

{% assign docker_lessons      = site.pages | where_exp: "p", "p.url contains '/docker/lessons/'" | sort: "url" %}
{% assign docker_labs         = site.pages | where_exp: "p", "p.url contains '/docker/labs/'" | sort: "url" %}
{% assign docker_cheatsheets  = site.pages | where_exp: "p", "p.url contains '/docker/cheatsheet/'" | sort: "url" %}
{% assign docker_classcode    = site.pages | where_exp: "p", "p.url contains '/docker/classcode/'" | sort: "url" %}
{% assign docker_pdfs         = site.static_files | where_exp: "f", "f.path contains '/docker/pdf/'" | where_exp: "f", "f.extname == '.pdf'" | sort: "path" %}

{% assign projects            = site.pages | where_exp: "p", "p.url contains '/projects/'" | sort: "url" %}

<style>
/* ── Reset & layout override ─────────────────────────────── */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
main.page, .page { all: unset !important; display: flex !important; flex-direction: column !important; height: 100vh !important; overflow: hidden !important; }

/* ── Design tokens ───────────────────────────────────────── */
:root {
  --bg:       #1e1e1e;
  --bar:      #2d2d2d;
  --side:     #252526;
  --hover:    #2a2d2e;
  --active:   #37373d;
  --border:   #3e3e42;
  --text:     #cccccc;
  --muted:    #858585;
  --accent:   #818cf8;
  --pink:     #ec4899;
  --green:    #4ec9b0;
  --blue:     #4fc3f7;
  --yellow:   #e2c08d;
  --orange:   #ce9178;
}

/* ── Typography ──────────────────────────────────────────── */
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }

/* ── Top bar ─────────────────────────────────────────────── */
.topbar {
  background: var(--bar);
  border-bottom: 1px solid var(--border);
  padding: 0 20px;
  height: 48px;
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
  z-index: 10;
}
.topbar-logo {
  font-size: 1rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: .5px;
}
.topbar-sep { width: 1px; height: 20px; background: var(--border); }
.topbar-chips { display: flex; gap: 6px; }
.chip {
  background: var(--active);
  border: 1px solid var(--border);
  padding: 3px 11px;
  border-radius: 20px;
  font-size: .75rem;
  color: var(--muted);
  cursor: default;
}
.chip.linux  { border-color: #4fc3f7; color: #4fc3f7; }
.chip.python { border-color: #4ec9b0; color: #4ec9b0; }
.chip.git      { border-color: #e2c08d; color: #e2c08d; }
.chip.docker   { border-color: #0db7ed; color: #0db7ed; }
.chip.projects { border-color: #f59e0b; color: #f59e0b; }

.topbar-hw {
  margin-left: auto;
  background: var(--accent);
  color: #fff;
  padding: 4px 14px;
  border-radius: 6px;
  font-size: .78rem;
  font-weight: 600;
  text-decoration: none;
  transition: opacity .15s;
}
.topbar-hw:hover { opacity: .85; }

/* ── Workspace ───────────────────────────────────────────── */
.workspace { display: flex; flex: 1; overflow: hidden; }

/* ── Sidebar ─────────────────────────────────────────────── */
.sidebar {
  width: 290px;
  background: var(--side);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-hdr {
  padding: 8px 14px 7px;
  font-size: .68rem;
  text-transform: uppercase;
  letter-spacing: 1.8px;
  color: var(--muted);
  font-weight: 700;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.tree { flex: 1; overflow-y: auto; padding: 6px 0; }
.tree::-webkit-scrollbar { width: 6px; }
.tree::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* subject row */
.t-subj {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: .875rem;
  font-weight: 600;
  transition: background .1s;
  user-select: none;
  border-left: 3px solid transparent;
}
.t-subj:hover { background: var(--hover); }
.t-subj.open  { border-left-color: var(--accent); }

/* category row */
.t-cat {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px 4px 26px;
  cursor: pointer;
  font-size: .825rem;
  color: #bbb;
  transition: background .1s;
  user-select: none;
}
.t-cat:hover { background: var(--hover); }
.t-cat.sel   { background: var(--active); color: var(--text); }

/* file row */
.t-file {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px 3px 42px;
  font-size: .78rem;
  color: var(--muted);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background .1s;
}
.t-file:hover { background: var(--hover); color: var(--text); }

/* arrow */
.arr {
  font-size: .58rem;
  color: var(--muted);
  transition: transform .15s;
  flex-shrink: 0;
  display: inline-block;
  width: 12px;
}
.arr.open { transform: rotate(90deg); }

/* count badge */
.cnt {
  margin-left: auto;
  font-size: .68rem;
  background: var(--border);
  color: var(--muted);
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: 400;
  flex-shrink: 0;
}

/* collapsible children */
.t-kids { display: none; }
.t-kids.open { display: block; }

/* ── Main content ────────────────────────────────────────── */
.main { flex: 1; overflow-y: auto; padding: 28px 32px; }
.main::-webkit-scrollbar { width: 6px; }
.main::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* welcome screen */
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: var(--muted);
  min-height: 300px;
}
.welcome h1 {
  font-size: 2.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent), var(--pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}
.welcome p { font-size: .95rem; margin-bottom: 28px; }
.welcome-pills { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.w-pill {
  border: 1px solid var(--border);
  background: var(--side);
  padding: 8px 18px;
  border-radius: 20px;
  font-size: .85rem;
  color: var(--text);
}

/* panel */
.panel { display: none; }
.panel.active { display: block; }

/* breadcrumb */
.bc {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: .82rem;
  color: var(--muted);
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}
.bc b { color: var(--text); font-weight: 600; }
.bc-sep { opacity: .45; }

/* file grid */
.fgrid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 12px;
}

/* file card */
.fcard {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--side);
  border: 1px solid var(--border);
  border-radius: 10px;
  text-decoration: none;
  color: var(--text);
  transition: all .15s ease;
  cursor: pointer;
}
.fcard:hover {
  border-color: var(--accent);
  background: var(--active);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(129,140,248,.18);
}
.fcard-ico { font-size: 1.8rem; flex-shrink: 0; line-height: 1; }
.fcard-info { flex: 1; min-width: 0; }
.fcard-name { font-size: .82rem; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fcard-type { font-size: .72rem; color: var(--muted); margin-top: 3px; }

/* empty state */
.empty { text-align: center; padding: 40px; color: var(--muted); font-size: .88rem; }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 640px) {
  .workspace { flex-direction: column; }
  .sidebar { width: 100%; height: 230px; border-right: none; border-bottom: 1px solid var(--border); }
  .fgrid { grid-template-columns: 1fr 1fr; }
  .topbar-chips { display: none; }
}
</style>

<!-- ═══════════════════════════ TOP BAR ═══════════════════════════ -->
<div class="topbar">
  <span style="font-size:1.1rem">📁</span>
  <span class="topbar-logo">DevSecOps-22</span>
  <div class="topbar-sep"></div>
  <div class="topbar-chips">
    <span class="chip linux">🐧 Linux</span>
    <span class="chip python">🐍 Python</span>
    <span class="chip git">🌿 GIT</span>
    <span class="chip docker">🐳 Docker</span>
    <span class="chip projects">🚀 Projects</span>
  </div>
  <a class="topbar-hw" href="{{ site.baseurl }}/homeworks/linux-homework/">📝 Homework</a>
</div>

<!-- ═══════════════════════════ WORKSPACE ═══════════════════════════ -->
<div class="workspace">

  <!-- ─── Sidebar Tree ─── -->
  <div class="sidebar">
    <div class="sidebar-hdr">Explorer</div>
    <div class="tree">

      <!-- ╔══ LINUX ══╗ -->
      <div class="t-subj" onclick="toggleSubj('linux',this)">
        <span class="arr" id="arr-linux">▶</span>
        <span>🐧</span><span>Linux</span>
        <span class="cnt">{{ linux_lessons.size | plus: linux_labs.size | plus: linux_cheatsheets.size | plus: linux_cheat_pdfs.size | plus: linux_pdfs.size }}</span>
      </div>
      <div class="t-kids" id="subj-linux">

        <div class="t-cat" onclick="openCat('linux-lessons',this)" id="cat-linux-lessons">
          <span class="arr" id="arr-linux-lessons">▶</span><span>📚</span><span>lessons</span>
          <span class="cnt">{{ linux_lessons.size }}</span>
        </div>
        <div class="t-kids" id="files-linux-lessons">
          {% for p in linux_lessons %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('linux-labs',this)" id="cat-linux-labs">
          <span class="arr" id="arr-linux-labs">▶</span><span>🔬</span><span>labs</span>
          <span class="cnt">{{ linux_labs.size }}</span>
        </div>
        <div class="t-kids" id="files-linux-labs">
          {% for p in linux_labs %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('linux-cheatsheets',this)" id="cat-linux-cheatsheets">
          <span class="arr" id="arr-linux-cheatsheets">▶</span><span>📋</span><span>cheatsheets</span>
          <span class="cnt">{{ linux_cheatsheets.size | plus: linux_cheat_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-linux-cheatsheets">
          {% for p in linux_cheatsheets %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
          {% for f in linux_cheat_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('linux-pdf',this)" id="cat-linux-pdf">
          <span class="arr" id="arr-linux-pdf">▶</span><span>📄</span><span>pdf</span>
          <span class="cnt">{{ linux_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-linux-pdf">
          {% for f in linux_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

      </div>

      <!-- ╔══ PYTHON ══╗ -->
      <div class="t-subj" onclick="toggleSubj('python',this)">
        <span class="arr" id="arr-python">▶</span>
        <span>🐍</span><span>Python</span>
        <span class="cnt">{{ python_lessons.size | plus: python_labs.size | plus: python_cheat_pdfs.size | plus: python_pdfs.size | plus: python_classcode.size }}</span>
      </div>
      <div class="t-kids" id="subj-python">

        <div class="t-cat" onclick="openCat('python-lessons',this)" id="cat-python-lessons">
          <span class="arr" id="arr-python-lessons">▶</span><span>📚</span><span>lessons</span>
          <span class="cnt">{{ python_lessons.size }}</span>
        </div>
        <div class="t-kids" id="files-python-lessons">
          {% for p in python_lessons %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('python-labs',this)" id="cat-python-labs">
          <span class="arr" id="arr-python-labs">▶</span><span>🔬</span><span>labs</span>
          <span class="cnt">{{ python_labs.size }}</span>
        </div>
        <div class="t-kids" id="files-python-labs">
          {% for p in python_labs %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('python-cheatsheets',this)" id="cat-python-cheatsheets">
          <span class="arr" id="arr-python-cheatsheets">▶</span><span>📋</span><span>cheatsheets</span>
          <span class="cnt">{{ python_cheat_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-python-cheatsheets">
          {% for f in python_cheat_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('python-pdf',this)" id="cat-python-pdf">
          <span class="arr" id="arr-python-pdf">▶</span><span>📄</span><span>pdf</span>
          <span class="cnt">{{ python_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-python-pdf">
          {% for f in python_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('python-classcode',this)" id="cat-python-classcode">
          <span class="arr" id="arr-python-classcode">▶</span><span>👨‍💻</span><span>classcode</span>
          <span class="cnt">{{ python_classcode.size }}</span>
        </div>
        <div class="t-kids" id="files-python-classcode">
          {% for f in python_classcode %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">🐍 {{ f.basename }}.py</a>{% endfor %}
        </div>

      </div>

      <!-- ╔══ PROJECTS ══╗ -->
      <div class="t-subj" onclick="toggleSubj('projects',this)">
        <span class="arr" id="arr-projects">▶</span>
        <span>🚀</span><span>Projects</span>
        <span class="cnt">{{ projects.size }}</span>
      </div>
      <div class="t-kids" id="subj-projects">

        <div class="t-cat" onclick="openCat('projects-files',this)" id="cat-projects-files">
          <span class="arr" id="arr-projects-files">▶</span><span>📁</span><span>projects</span>
          <span class="cnt">{{ projects.size }}</span>
        </div>
        <div class="t-kids" id="files-projects-files">
          {% for p in projects %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

      </div>

      <!-- ╔══ GIT ══╗ -->
      <div class="t-subj" onclick="toggleSubj('git',this)">
        <span class="arr" id="arr-git">▶</span>
        <span>🌿</span><span>GIT</span>
        <span class="cnt">{{ git_lessons.size | plus: git_pdfs.size }}</span>
      </div>
      <div class="t-kids" id="subj-git">

        <div class="t-cat" onclick="openCat('git-lessons',this)" id="cat-git-lessons">
          <span class="arr" id="arr-git-lessons">▶</span><span>📚</span><span>lessons</span>
          <span class="cnt">{{ git_lessons.size }}</span>
        </div>
        <div class="t-kids" id="files-git-lessons">
          {% for p in git_lessons %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('git-pdf',this)" id="cat-git-pdf">
          <span class="arr" id="arr-git-pdf">▶</span><span>📄</span><span>pdf</span>
          <span class="cnt">{{ git_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-git-pdf">
          {% for f in git_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

      </div>

      <!-- ╔══ DOCKER ══╗ -->
      <div class="t-subj" onclick="toggleSubj('docker',this)">
        <span class="arr" id="arr-docker">▶</span>
        <span>🐳</span><span>Docker</span>
        <span class="cnt">{{ docker_lessons.size | plus: docker_labs.size | plus: docker_cheatsheets.size | plus: docker_classcode.size | plus: docker_pdfs.size }}</span>
      </div>
      <div class="t-kids" id="subj-docker">

        <div class="t-cat" onclick="openCat('docker-lessons',this)" id="cat-docker-lessons">
          <span class="arr" id="arr-docker-lessons">▶</span><span>📚</span><span>lessons</span>
          <span class="cnt">{{ docker_lessons.size }}</span>
        </div>
        <div class="t-kids" id="files-docker-lessons">
          {% for p in docker_lessons %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('docker-labs',this)" id="cat-docker-labs">
          <span class="arr" id="arr-docker-labs">▶</span><span>🔬</span><span>labs</span>
          <span class="cnt">{{ docker_labs.size }}</span>
        </div>
        <div class="t-kids" id="files-docker-labs">
          {% for p in docker_labs %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('docker-cheatsheets',this)" id="cat-docker-cheatsheets">
          <span class="arr" id="arr-docker-cheatsheets">▶</span><span>📋</span><span>cheatsheets</span>
          <span class="cnt">{{ docker_cheatsheets.size }}</span>
        </div>
        <div class="t-kids" id="files-docker-cheatsheets">
          {% for p in docker_cheatsheets %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('docker-classcode',this)" id="cat-docker-classcode">
          <span class="arr" id="arr-docker-classcode">▶</span><span>👨‍💻</span><span>classcode</span>
          <span class="cnt">{{ docker_classcode.size }}</span>
        </div>
        <div class="t-kids" id="files-docker-classcode">
          {% for p in docker_classcode %}<a class="t-file" href="{{ site.baseurl }}{{ p.url }}">📝 {{ p.title | default: p.name }}</a>{% endfor %}
        </div>

        <div class="t-cat" onclick="openCat('docker-pdf',this)" id="cat-docker-pdf">
          <span class="arr" id="arr-docker-pdf">▶</span><span>📄</span><span>pdf</span>
          <span class="cnt">{{ docker_pdfs.size }}</span>
        </div>
        <div class="t-kids" id="files-docker-pdf">
          {% for f in docker_pdfs %}<a class="t-file" href="{{ site.baseurl }}{{ f.path }}" target="_blank">📄 {{ f.basename }}</a>{% endfor %}
        </div>

      </div>

    </div>

  </div><!-- /sidebar -->

  <!-- ─── Main Panel ─── -->
  <div class="main" id="main">

    <!-- Welcome -->
    <div class="welcome" id="welcome">
      <h1>DevSecOps-22</h1>
      <p>Click any folder in the explorer to browse its files</p>
      <div class="welcome-pills">
        <span class="w-pill">🐧 Linux</span>
        <span class="w-pill">🐍 Python</span>
        <span class="w-pill">🌿 GIT</span>
        <span class="w-pill">� Docker</span>
        <span class="w-pill">� Projects</span>
      </div>
    </div>

    <!-- ── Linux panels ── -->
    <div class="panel" id="panel-linux-lessons">
      <div class="bc">🐧 Linux <span class="bc-sep">›</span> <b>📚 Lessons</b></div>
      <div class="fgrid">
        {% for p in linux_lessons %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📝</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lesson</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-linux-labs">
      <div class="bc">🐧 Linux <span class="bc-sep">›</span> <b>🔬 Labs</b></div>
      <div class="fgrid">
        {% for p in linux_labs %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">🔬</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lab</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-linux-cheatsheets">
      <div class="bc">🐧 Linux <span class="bc-sep">›</span> <b>📋 Cheatsheets</b></div>
      <div class="fgrid">
        {% for p in linux_cheatsheets %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📋</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Cheatsheet</div>
          </div>
        </a>
        {% endfor %}
        {% for f in linux_cheat_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📄</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Cheatsheet</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-linux-pdf">
      <div class="bc">🐧 Linux <span class="bc-sep">›</span> <b>📄 PDF Resources</b></div>
      <div class="fgrid">
        {% for f in linux_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📄</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Document</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <!-- ── Python panels ── -->
    <div class="panel" id="panel-python-lessons">
      <div class="bc">🐍 Python <span class="bc-sep">›</span> <b>📚 Lessons</b></div>
      <div class="fgrid">
        {% for p in python_lessons %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📝</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lesson</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-python-labs">
      <div class="bc">🐍 Python <span class="bc-sep">›</span> <b>🔬 Labs</b></div>
      <div class="fgrid">
        {% for p in python_labs %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">🔬</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lab</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-python-cheatsheets">
      <div class="bc">🐍 Python <span class="bc-sep">›</span> <b>📋 Cheatsheets</b></div>
      <div class="fgrid">
        {% for f in python_cheat_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📋</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Cheatsheet</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-python-pdf">
      <div class="bc">🐍 Python <span class="bc-sep">›</span> <b>📄 PDF Resources</b></div>
      <div class="fgrid">
        {% for f in python_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📄</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Document</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-python-classcode">
      <div class="bc">🐍 Python <span class="bc-sep">›</span> <b>👨‍💻 Class Code</b></div>
      <div class="fgrid">
        {% for f in python_classcode %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">🐍</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename }}.py</div>
            <div class="fcard-type">Python · Script</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <!-- ── Projects panels ── -->
    <div class="panel" id="panel-projects-files">
      <div class="bc">🚀 Projects <span class="bc-sep">›</span> <b>📁 Projects</b></div>
      <div class="fgrid">
        {% for p in projects %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">🚀</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Project</div>
          </div>
        </a>
        {% else %}
        <div class="empty">No projects published yet</div>
        {% endfor %}
      </div>
    </div>

    <!-- ── GIT panels ── -->
    <div class="panel" id="panel-git-lessons">
      <div class="bc">🌿 GIT <span class="bc-sep">›</span> <b>📚 Lessons</b></div>
      <div class="fgrid">
        {% for p in git_lessons %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📝</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lesson</div>
          </div>
        </a>
        {% else %}
        <div class="empty">No lessons published yet</div>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-git-pdf">
      <div class="bc">🌿 GIT <span class="bc-sep">›</span> <b>📄 PDF Resources</b></div>
      <div class="fgrid">
        {% for f in git_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📄</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Document</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <!-- ── Docker panels ── -->
    <div class="panel" id="panel-docker-lessons">
      <div class="bc">🐳 Docker <span class="bc-sep">›</span> <b>📚 Lessons</b></div>
      <div class="fgrid">
        {% for p in docker_lessons %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📝</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lesson</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-docker-labs">
      <div class="bc">🐳 Docker <span class="bc-sep">›</span> <b>🔬 Labs</b></div>
      <div class="fgrid">
        {% for p in docker_labs %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">🔬</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Lab</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-docker-cheatsheets">
      <div class="bc">🐳 Docker <span class="bc-sep">›</span> <b>📋 Cheatsheets</b></div>
      <div class="fgrid">
        {% for p in docker_cheatsheets %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">📋</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Cheatsheet</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-docker-classcode">
      <div class="bc">🐳 Docker <span class="bc-sep">›</span> <b>👨‍💻 Class Code</b></div>
      <div class="fgrid">
        {% for p in docker_classcode %}
        <a class="fcard" href="{{ site.baseurl }}{{ p.url }}">
          <span class="fcard-ico">👨‍💻</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ p.title | default: p.name }}</div>
            <div class="fcard-type">Markdown · Class Code</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

    <div class="panel" id="panel-docker-pdf">
      <div class="bc">🐳 Docker <span class="bc-sep">›</span> <b>📄 PDF Resources</b></div>
      <div class="fgrid">
        {% for f in docker_pdfs %}
        <a class="fcard" href="{{ site.baseurl }}{{ f.path }}" target="_blank">
          <span class="fcard-ico">📄</span>
          <div class="fcard-info">
            <div class="fcard-name">{{ f.basename | replace: '-', ' ' | replace: '_', ' ' }}</div>
            <div class="fcard-type">PDF · Document</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>

  </div><!-- /main -->
</div><!-- /workspace -->

<script>
var activePanel = null;
var activeCat   = null;

function toggleSubj(id, el) {
  var kids = document.getElementById('subj-' + id);
  var arr  = document.getElementById('arr-' + id);
  kids.classList.toggle('open');
  arr.classList.toggle('open');
  el.classList.toggle('open');
}

function openCat(id, catEl) {
  var treeKids = document.getElementById('files-' + id);
  var arr      = document.getElementById('arr-' + id);
  treeKids.classList.toggle('open');
  arr.classList.toggle('open');

  if (activeCat) activeCat.classList.remove('sel');
  catEl.classList.add('sel');
  activeCat = catEl;

  document.getElementById('welcome').style.display = 'none';
  if (activePanel) activePanel.classList.remove('active');
  activePanel = document.getElementById('panel-' + id);
  if (activePanel) activePanel.classList.add('active');
}
</script>
