# Tech Cafe series — BigMarker template

Recurring live series the user runs weekly-ish on BigMarker channel `coursekub`. Use as the default template for new Tech Cafe episodes (and similar recurring live series).

## Channel & identity
- **Channel_id:** `coursekub` (landing/channel URL prefix `https://www.bigmarker.com/coursekub/...`)
- **Title pattern:** `[Tech Cafe] AI Chat with Boy & Perth EP.N`
- **Episode slot:** Saturdays, normally 10:00–11:30 **Bangkok** (+07:00), 90 min duration
- **Description (`purpose`) style** — bilingual Thai block, structure:
  ```
  วัน-เวลา: อาทิตย์ <D> เดือน <YYYY> เวลา 10-11 โมง

  ไลฟ์ของ Tech Cafe เราจะมาคุยกันเรื่อง
  - <topic line(s)>
  - Ask me anything with Boy & Perth ถามตอบกันสบาย ๆ
  ```
  When the topic is TBD at creation, put a placeholder line like `- TBD (หัวข้อจะประกาศภายหลัง)` and update later.

## Template settings (that carry over when copying an episode)
- `privacy: private`
- `max_attendance: 1100`
- `webcast_mode: required`
- `time_zone: Bangkok`
- `language: English`
- `enable_registration_email: true`, `enable_ie_safari: true` (EP4 had Safari on; the copy may reset to false — confirm via GET if it matters)

## Presenters (all three preserved by the copy)
| Display name | Email | Role |
|---|---|---|
| Perth - Tech Cafe | woratana.n@gmail.com | moderator + can_manage |
| Boy - Tech Cafe | L.varayut@gmail.com | moderator |
| Perth - Tech Cafe (host2) | woratana.n+host2@gmail.com | moderator + can_manage |

## Episode history (as of Aug 2026)
| EP | BigMarker id | Date (Bangkok) | Duration |
|---|---|---|---|
| Practice w/ Perth | dca4cea4cd1d | Tue 14 Apr 2026, 10:35 (+10:00) | 90 |
| EP.1 | ff93ac67a6c4 | Sun 19 Apr 2026, 10:00 | 90 |
| EP.2 | 77e1c3594214 | Sun 17 May 2026, 10:00 | 90 |
| EP.3 | 7bcee416b36e | Sun 21 Jun 2026, 10:00 | 90 |
| EP.4 (latest template) | 2f707cb90de8 | Sun 26 Jul 2026, 10:00 | 90 |
| EP.5 (created Aug 2026) | 7660462282b3 | Sat 12 Sep 2026, 10:00 | 90 |

**Copy chain:** each episode was itself created by copying the prior one (`copy_webinar_id`). EP.5 was copied from EP.4 (id `2f707cb90de8`).

## Verification recipe
After creating EP.N, GET `$BASE/conferences/<new-id>` and confirm: all 3 presenters present, `start_time`/`duration`/`time_zone`, `privacy`, and `conference_address` = `https://www.bigmarker.com/coursekub/tech-cafe-ai-chat-with-boy-perth-ep-N`.
