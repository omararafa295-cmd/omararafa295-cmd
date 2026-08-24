<p align="center">
  <picture>
    <source media="(max-width: 760px) and (prefers-color-scheme: dark)" srcset="./assets/hero/omar-profile-v3-mobile-dark.svg">
    <source media="(max-width: 760px)" srcset="./assets/hero/omar-profile-v3-mobile-light.svg">
    <source media="(prefers-color-scheme: dark)" srcset="./assets/hero/omar-profile-v3-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/hero/omar-profile-v3-light.svg">
    <img src="./assets/hero/omar-profile-v3-dark.svg" alt="Omar Arafa, Full Stack PHP Developer" width="100%">
  </picture>
</p>

<div align="center">

<a href="https://omararafa295-cmd.github.io/Omar-Arafa-Portfolio/index.html">
  <img src="https://img.shields.io/badge/Portfolio-0D1117?style=for-the-badge&logo=googlechrome&logoColor=58A6FF" alt="Portfolio" />
</a>
<a href="https://linkedin.com/in/omar-arafa-641504358/">
  <img src="https://img.shields.io/badge/LinkedIn-0D1117?style=for-the-badge&logo=linkedin&logoColor=58A6FF" alt="LinkedIn" />
</a>
<a href="mailto:omararafa294@gmail.com">
  <img src="https://img.shields.io/badge/Email-0D1117?style=for-the-badge&logo=gmail&logoColor=58A6FF" alt="Email" />
</a>

</div>

---

## `~/core-logic` — Who Am I?

```php
<?php

namespace App\Engineers;

use Tech\Software\Laravel;
use Tech\Hardware\EmbeddedSystems;

class OmarArafa implements FullStackInterface, ControlSystemsInterface
{
    use ProblemSolving;

    private string $university = 'Zagazig University';
    private string $major = 'Computer & Systems Engineering';
    private int $academicYear = 3;

    public function getSystemStatus(): array
    {
        return [
            'Current Focus' => 'Architecting scalable backend solutions & IoT integration',
            'Architecture'  => ['MVC', 'Service-Oriented', 'RESTful APIs'],
            'Hardware Core' => 'PID Controllers, Sensor Integration, Microcontrollers',
        ];
    }

    public function executeDailyProcess(string $currentTask): string
    {
        return match ($currentTask) {
            'backend'  => Laravel::buildScalableAPI()->optimizeQueries(),
            'hardware' => EmbeddedSystems::tunePID()->deployToArduino(),
            'learning' => $this->absorbNewTechnologies(),
            default    => 'Compiling code and drinking coffee... ☕'
        };
    }
}
```

---

## `~/stack` — Build Environment

<div align="center">

<img src="https://skillicons.dev/icons?i=php,laravel,mysql,html,css,js,bootstrap,git,github,vscode,arduino&theme=dark" alt="Tech Stack" />

</div>

<br>

<table align="center">
  <tr>
    <td><b>Backend</b></td>
    <td>PHP • Laravel • RESTful APIs • MySQL</td>
  </tr>
  <tr>
    <td><b>Frontend</b></td>
    <td>HTML • CSS • JavaScript • Bootstrap</td>
  </tr>
  <tr>
    <td><b>Architecture</b></td>
    <td>MVC • Service-Oriented Design</td>
  </tr>
  <tr>
    <td><b>Hardware</b></td>
    <td>PID Controllers • Sensor Integration • Microcontrollers • IoT</td>
  </tr>
  <tr>
    <td><b>Toolchain</b></td>
    <td>Git • GitHub • VS Code • Arduino</td>
  </tr>
</table>

---

## `~/status` — Current Focus

```text
[01] Building scalable Laravel backends
[02] Improving database and API architecture
[03] Connecting software systems with embedded hardware
[04] Learning through practical engineering projects
```

---

<div align="center">

### `omar@developer:~$ keep_building_`

<img width="49%" src="https://github-readme-stats.vercel.app/api?username=omararafa295-cmd&show_icons=true&theme=github_dark&hide_border=true&bg_color=00000000&title_color=58A6FF&text_color=E6EDF3&icon_color=58A6FF&rank_icon=github" alt="GitHub Stats" />
<img width="49%" src="https://streak-stats.demolab.com?user=omararafa295-cmd&theme=github-dark-blue&hide_border=true&background=00000000&ring=58A6FF&fire=58A6FF&currStreakLabel=58A6FF&sideNums=E6EDF3&currStreakNum=E6EDF3&sideLabels=8B949E&dates=8B949E" alt="GitHub Streak" />

<br><br>

<img width="55%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=omararafa295-cmd&layout=compact&theme=github_dark&hide_border=true&bg_color=00000000&title_color=58A6FF&text_color=E6EDF3" alt="Top Languages" />

<br><br>

<img src="https://komarev.com/ghpvc/?username=omararafa295-cmd&label=PROFILE+VIEWS&color=1f6feb&style=flat-square" alt="Profile Views" />

</div>