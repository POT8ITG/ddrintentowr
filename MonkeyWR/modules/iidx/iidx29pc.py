from tinydb import Query, where

import config
import random

from fastapi import APIRouter, Request, Response

from core_common import core_process_request, core_prepare_response, E
from core_database import get_db

router = APIRouter(prefix="/local2", tags=["local2"])
router.model_whitelist = ["LDJ"]


def get_profile(cid):
    return get_db().table('iidx_profile').get(
        where('card') == cid
    )


def get_game_profile(cid, game_version):
    profile = get_profile(cid)

    return profile['version'].get(str(game_version), None)


def get_id_from_profile(cid):
    profile = get_db().table('iidx_profile').get(
        where('card') == cid
    )

    djid = "%08d" % profile['iidx_id']
    djid_split = '-'.join([djid[:4], djid[4:]])

    return profile['iidx_id'], djid_split


def calculate_folder_mask(profile):
    return profile.get('_show_category_grade', 0) << 0 \
           | (profile.get('_show_category_status', 0) << 1) \
           | (profile.get('_show_category_difficulty', 0) << 2) \
           | (profile.get('_show_category_alphabet', 0) << 3) \
           | (profile.get('_show_category_rival_play', 0) << 4) \
           | (profile.get('_show_category_rival_winlose', 0) << 6) \
           | (profile.get('_show_rival_shop_info', 0) << 7) \
           | (profile.get('_hide_play_count', 0) << 8) \
           | (profile.get('_show_score_graph_cutin', 0) << 9) \
           | (profile.get('_classic_hispeed', 0) << 10) \
           | (profile.get('_hide_iidx_id', 0) << 12)


@router.post('/{gameinfo}/IIDX29pc/get')
async def iidx29pc_get(request: Request):
    request_info = await core_process_request(request)
    game_version = request_info['game_version']

    cid = request_info['root'][0].attrib['cid']
    profile = get_game_profile(cid, game_version)
    djid, djid_split = get_id_from_profile(cid)

    response = E.response(
        E.IIDX29pc(
            E.pcdata(
                d_auto_adjust=profile['d_auto_adjust'],
                d_auto_scrach=profile['d_auto_scrach'],
                d_camera_layout=profile['d_camera_layout'],
                d_disp_judge=profile['d_disp_judge'],
                d_exscore=profile['d_exscore'],
                d_gauge_disp=profile['d_gauge_disp'],
                d_ghost_score=profile['d_ghost_score'],
                d_gno=profile['d_gno'],
                d_graph_score=profile['d_graph_score'],
                d_gtype=profile['d_gtype'],
                d_hispeed=profile['d_hispeed'],
                d_judge=profile['d_judge'],
                d_judgeAdj=profile['d_judgeAdj'],
                d_lane_brignt=profile['d_lane_brignt'],
                d_liflen=profile['d_liflen'],
                d_notes=profile['d_notes'],
                d_opstyle=profile['d_opstyle'],
                d_pace=profile['d_pace'],
                d_sdlen=profile['d_sdlen'],
                d_sdtype=profile['d_sdtype'],
                d_sorttype=profile['d_sorttype'],
                d_sub_gno=profile['d_sub_gno'],
                d_timing=profile['d_timing'],
                d_tsujigiri_disp=profile['d_tsujigiri_disp'],
                d_tune=profile['d_tune'],
                dach=profile['dach'],
                dp_opt=profile['dp_opt'],
                dp_opt2=profile['dp_opt2'],
                dpnum=profile["dpnum"],
                gpos=profile['gpos'],
                id=djid,
                idstr=djid_split,
                mode=profile['mode'],
                name=profile['djname'],
                ngrade=profile['ngrade'],
                pid=profile['region'],
                pmode=profile['pmode'],
                rtype=profile['rtype'],
                s_auto_adjust=profile['s_auto_adjust'],
                s_auto_scrach=profile['s_auto_scrach'],
                s_camera_layout=profile['s_camera_layout'],
                s_disp_judge=profile['s_disp_judge'],
                s_exscore=profile['s_exscore'],
                s_gauge_disp=profile['s_gauge_disp'],
                s_ghost_score=profile['s_ghost_score'],
                s_gno=profile['s_gno'],
                s_graph_score=profile['s_graph_score'],
                s_gtype=profile['s_gtype'],
                s_hispeed=profile['s_hispeed'],
                s_judge=profile['s_judge'],
                s_judgeAdj=profile['s_judgeAdj'],
                s_lane_brignt=profile['s_lane_brignt'],
                s_liflen=profile['s_liflen'],
                s_notes=profile['s_notes'],
                s_opstyle=profile['s_opstyle'],
                s_pace=profile['s_pace'],
                s_sdlen=profile['s_sdlen'],
                s_sdtype=profile['s_sdtype'],
                s_sorttype=profile['s_sorttype'],
                s_sub_gno=profile['s_sub_gno'],
                s_timing=profile['s_timing'],
                s_tsujigiri_disp=profile['s_tsujigiri_disp'],
                s_tune=profile['s_tune'],
                sach=profile['sach'],
                sp_opt=profile['sp_opt'],
                spnum=profile['spnum'],
            ),
            E.qprodata([profile["head"], profile["hair"], profile["face"], profile["hand"], profile["body"]],
                       __type="u32", __size=5 * 4),
            E.skin(
                [
                    profile["frame"],
                    profile["turntable"],
                    profile["explosion"],
                    profile["bgm"],
                    calculate_folder_mask(profile),
                    profile["sudden"],
                    profile["judge_pos"],
                    profile["categoryvoice"],
                    profile["note"],
                    profile["fullcombo"],
                    profile["keybeam"],
                    profile["judgestring"],
                    -1,
                    profile["soundpreview"],
                    profile["grapharea"],
                    profile["effector_lock"],
                    profile["effector_type"],
                    profile["explosion_size"],
                    profile["alternate_hcn"],
                    profile["kokokara_start"],
                ],
                __type="s16"),
            E.rlist(),
            E.ir_data(),
            E.secret_course_data(),
            E.deller(deller=profile['deller'], rate=0),
            E.secret(
                E.flg1(profile.get('secret_flg1', [-1, -1, -1]), __type="s64"),
                E.flg2(profile.get('secret_flg2', [-1, -1, -1]), __type="s64"),
                E.flg3(profile.get('secret_flg3', [-1, -1, -1]), __type="s64"),
                E.flg4(profile.get('secret_flg4', [-1, -1, -1]), __type="s64"),
            ),
            E.join_shop(join_cflg=1, join_id=10, join_name=config.arcade, joinflg=1),
            E.leggendaria(E.flg1(profile.get('leggendaria_flg1', [-1, -1, -1]), __type="s64")),
            E.grade(
                *[E.g(x, __type="u8") for x in profile['grade_values']],
                dgid=profile['grade_double'],
                sgid=profile['grade_single'],
            ),
            E.world_tourism_secret_flg(
                E.flg1(profile.get('wt_flg1', [-1, -1, -1]), __type="s64"),
                E.flg2(profile.get('wt_flg2', [-1, -1, -1]), __type="s64"),
            ),
            E.lightning_setting(
                E.slider(profile.get('lightning_setting_slider', [0] * 7), __type="s32"),
                E.light(profile.get('lightning_setting_light', [1] * 10), __type="bool"),
                E.concentration(profile.get('lightning_setting_concentration', 0), __type="bool"),
                headphone_vol=profile.get('lightning_setting_headphone_vol', 0),
                resistance_sp_left=profile.get('lightning_setting_resistance_sp_left', 0),
                resistance_sp_right=profile.get('lightning_setting_resistance_sp_right', 0),
                resistance_dp_left=profile.get('lightning_setting_resistance_dp_left', 0),
                resistance_dp_right=profile.get('lightning_setting_resistance_dp_right', 0),
                skin_0=profile.get('lightning_setting_skin_0', 0),
                flg_skin_0=profile.get('lightning_setting_flg_skin_0', 0),
            ),
            E.arena_data(
                E.achieve_data(
                    arena_class=-1,
                    counterattack_num=0,
                    best_top_class_continuing=0,
                    now_top_class_continuing=0,
                    play_style=0,
                    rating_value=90,
                ),
                E.achieve_data(
                    arena_class=-1,
                    counterattack_num=0,
                    best_top_class_continuing=0,
                    now_top_class_continuing=0,
                    play_style=1,
                    rating_value=90,
                ),
                E.cube_data(
                    cube=200,
                    season_id=0,
                ),
                play_num=6,
                play_num_dp=3,
                play_num_sp=3,
                prev_best_class_sp=18,
                prev_best_class_dp=18,
            ),
            E.follow_data(),
            E.classic_course_data(),
            E.bind_eaappli(),
            E.ea_premium_course(),
            E.enable_qr_reward(),
            E.nostalgia_open(),
            E.event_1(
                story_prog=profile.get('event_1_story_prog', 0),
                last_select_area=profile.get('event_1_last_select_area', 0),
                failed_num=profile.get('event_1_failed_num', 0),
                event_play_num=profile.get('event_1_event_play_num', 0),
                last_select_area_id=profile.get('event_1_last_select_area_id', 0),
                last_select_platform_type=profile.get('event_1_last_select_platform_type', 0),
                last_select_platform_id=profile.get('event_1_last_select_platform_id', 0),
            ),
            E.language_setting(language=profile['language_setting']),
            E.movie_agreement(agreement_version=profile['movie_agreement']),
            E.bpl_virtual(),
            E.lightning_play_data(spnum=profile['lightning_play_data_spnum'],
                                  dpnum=profile['lightning_play_data_dpnum']),
            E.weekly(
                mid=-1,
                wid=1,
            ),
            E.packinfo(
                music_0=-1,
                music_1=-1,
                music_2=-1,
                pack_id=1,
            ),
            E.kac_entry_info(
                E.enable_kac_deller(),
                E.disp_kac_mark(),
                E.open_kac_common_music(),
                E.open_kac_new_a12_music(),
                E.is_kac_entry(),
                E.is_kac_evnet_entry(),
            ),
            E.orb_data(rest_orb=100, present_orb=100),
            E.visitor(anum=1, pnum=2, snum=1, vs_flg=1),
            E.tonjyutsu(black_pass=-1, platinum_pass=-1),
            E.pay_per_use(item_num=99),
            E.old_linkage_secret_flg(
                floor_infection4=-1,
                bemani_janken=-1,
                ichika_rush=-1,
                nono_rush=-1,
                song_battle=-1,
            ),
            E.floor_infection4(music_list=-1),
            E.bemani_vote(music_list=-1),
            E.bemani_janken_meeting(music_list=-1),
            E.bemani_rush(music_list_ichika=-1, music_list_nono=-1),
            E.ultimate_mobile_link(music_list=-1),
            E.bemani_musiq_fes(music_list=-1),
            E.busou_linkage(music_list=-1),
            E.busou_linkage_2(music_list=-1),
            E.valkyrie_linkage_data(progress=-1),
            E.valkyrie_linkage_2_data(progress=-1),
            E.achievements(
                E.trophy(
                    profile.get('achievements_trophy', [])[:20],
                    __type="s64"
                ),
                pack=profile.get('achievements_pack_id', 0),
                pack_comp=profile.get('achievements_pack_comp', 0),
                last_weekly=profile.get('achievements_last_weekly', 0),
                weekly_num=profile.get('achievements_weekly_num', 0),
                visit_flg=profile.get('achievements_visit_flg', 0),
                rival_crush=0,
            ),
            E.notes_radar(
                E.radar_score(
                    profile['notes_radar_single'],
                    __type="s32",
                ),
                style=0,
            ),
            E.notes_radar(
                E.radar_score(
                    profile['notes_radar_double'],
                    __type="s32",
                ),
                style=1,
            ),
            E.dj_rank(
                E.rank(
                    profile['dj_rank_single_rank'],
                    __type="s32",
                ),
                E.point(
                    profile['dj_rank_single_point'],
                    __type="s32",
                ),
                style=0,
            ),
            E.dj_rank(
                E.rank(
                    profile['dj_rank_double_rank'],
                    __type="s32",
                ),
                E.point(
                    profile['dj_rank_double_point'],
                    __type="s32",
                ),
                style=1,
            ),
            E.step(
                E.is_track_ticket(
                    profile['stepup_is_track_ticket'],
                    __type="bool",
                ),
                dp_level=profile['stepup_dp_level'],
                dp_mplay=profile['stepup_dp_mplay'],
                enemy_damage=profile['stepup_enemy_damage'],
                enemy_defeat_flg=profile['stepup_enemy_defeat_flg'],
                mission_clear_num=profile['stepup_mission_clear_num'],
                progress=profile['stepup_progress'],
                sp_level=profile['stepup_sp_level'],
                sp_mplay=profile['stepup_sp_mplay'],
                tips_read_list=profile['stepup_tips_read_list'],
                total_point=profile['stepup_total_point'],
            ),
            E.skin_customize_flg(
                skin_frame_flg=profile['skin_customize_flag_frame'],
                skin_bgm_flg=profile['skin_customize_flag_bgm'],
                skin_lane_flg3=profile['skin_customize_flag_lane'],
            )
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/common')
async def iidx29pc_common(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc(
            E.monthly_mranking(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                __type="u16"),
            E.total_mranking(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                __type="u16"),
            # E.internet_ranking(),
            # E.secret_ex_course(),
            E.kac_mid([-1, -1, -1, -1, -1], __type="s32"),
            E.kac_clid([2, 2, 2, 2, 2], __type="s32"),
            E.ir(beat=3),
            E.cm(compo='cm_ultimate', folder='cm_ultimate', id=0),
            E.tdj_cm(
                E.cm(filename='cm_bn_001', id=0),
                E.cm(filename='cm_bn_002', id=1),
                E.cm(filename='event_bn_001', id=2),
                E.cm(filename='event_bn_004', id=3),
                E.cm(filename='event_bn_006', id=4),
                E.cm(filename='fipb_001', id=5),
                E.cm(filename='year_bn_004', id=6),
                E.cm(filename='year_bn_005', id=7),
                E.cm(filename='year_bn_006_2', id=8),
                E.cm(filename='year_bn_007', id=9),
            ),
            # E.playvideo_disable_music(E.music(musicid=-1)),
            # E.music_movie_suspend(E.music(music_id=-1, kind=0, name='')),
            # E.bpl_virtual(),
            E.movie_agreement(version=1),
            E.license('None', __type="str"),
            E.file_recovery(url=str(config.ip)),
            E.movie_upload(url=str(config.ip)),
            # E.button_release_frame(frame=''),
            # E.trigger_logic_type(type=''),
            # E.cm_movie_info(type=''),
            E.escape_package_info(),
            # E.expert(phase=1),
            # E.expert_random_secret(phase=1),
            E.boss(phase=0),  # disable event
            E.vip_pass_black(),
            E.eisei(open=1),
            E.deller_bonus(open=1),
            E.newsong_another(open=1),
            # E.pcb_check(flg=0)
            E.expert_secret_full_open(),
            E.eaorder_phase(phase=-1),
            E.common_evnet(flg=-1),
            E.system_voice_phase(phase=random.randint(1, 10)),  # TODO: Figure out range
            E.extra_boss_event(phase=6),
            E.event1_phase(phase=4),
            E.premium_area_news(open=1),
            E.premium_area_qpro(open=1),
            # E.disable_same_triger(frame=-1),
            E.play_video(),
            E.world_tourism(open_list=1),
            E.bpl_battle(phase=1),
            E.display_asio_logo(),
            # E.force_rom_check(),
            E.lane_gacha(),
            # E.fps_fix(),
            # E.save_unsync_log(),
            expire=600
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/save')
async def iidx29pc_save(request: Request):
    request_info = await core_process_request(request)
    game_version = request_info['game_version']

    xid = int(request_info['root'][0].attrib['iidxid'])
    cid = request_info['root'][0].attrib['cid']
    clt = int(request_info['root'][0].attrib['cltype'])

    profile = get_profile(cid)
    game_profile = profile['version'].get(str(game_version), {})

    for k in [
        'd_auto_adjust',
        'd_auto_scrach',
        'd_camera_layout',
        'd_disp_judge',
        'd_gauge_disp',
        'd_ghost_score',
        'd_gno',
        'd_graph_score',
        'd_gtype',
        'd_hispeed',
        'd_judge',
        'd_judgeAdj',
        'd_lane_brignt',
        'd_notes',
        'd_opstyle',
        'd_pace',
        'd_sdlen',
        'd_sdtype',
        'd_sorttype',
        'd_sub_gno',
        'd_timing',
        'd_tsujigiri_disp',
        'dp_opt',
        'dp_opt2',
        'gpos',
        'mode',
        'ngrade',
        'pmode',
        'rtype',
        's_auto_adjust',
        's_auto_scrach',
        's_camera_layout',
        's_disp_judge',
        's_gauge_disp',
        's_ghost_score',
        's_gno',
        's_graph_score',
        's_gtype',
        's_hispeed',
        's_judge',
        's_judgeAdj',
        's_lane_brignt',
        's_notes',
        's_opstyle',
        's_pace',
        's_sdlen',
        's_sdtype',
        's_sorttype',
        's_sub_gno',
        's_timing',
        's_tsujigiri_disp',
        'sp_opt',
    ]:
        if k in request_info['root'][0].attrib:
            game_profile[k] = request_info['root'][0].attrib[k]

    for k in [
        ('d_liflen', 'd_lift'),
        ('dach', 'd_achi'),
        ('s_liflen', 's_lift'),
        ('sach', 's_achi'),
    ]:
        if k[1] in request_info['root'][0].attrib:
            game_profile[k[0]] = request_info['root'][0].attrib[k[1]]

    lightning_setting = request_info['root'][0].find('lightning_setting')
    if lightning_setting is not None:
        for k in [
            'headphone_vol',
            'resistance_dp_left',
            'resistance_dp_right',
            'resistance_sp_left',
            'resistance_sp_right',
        ]:
            game_profile['lightning_setting_' + k] = int(lightning_setting.attrib[k])

        slider = lightning_setting.find('slider')
        if slider is not None:
            game_profile['lightning_setting_slider'] = [int(x) for x in slider.text.split(' ')]

        light = lightning_setting.find('light')
        if light is not None:
            game_profile['lightning_setting_light'] = [int(x) for x in light.text.split(' ')]

        concentration = lightning_setting.find('concentration')
        if concentration is not None:
            game_profile['lightning_setting_concentration'] = int(concentration.text)

    lightning_customize_flg = request_info['root'][0].find('lightning_customize_flg')
    if lightning_customize_flg is not None:
        for k in [
            'flg_skin_0',
        ]:
            game_profile['lightning_setting_' + k] = int(lightning_customize_flg.attrib[k])

    secret = request_info['root'][0].find('secret')
    if secret is not None:
        for k in ['flg1', 'flg2', 'flg3', 'flg4']:
            flg = secret.find(k)
            if flg is not None:
                game_profile['secret_' + k] = [int(x) for x in flg.text.split(' ')]

    leggendaria = request_info['root'][0].find('leggendaria')
    if leggendaria is not None:
        for k in ['flg1']:
            flg = leggendaria.find(k)
            if flg is not None:
                game_profile['leggendaria_' + k] = [int(x) for x in flg.text.split(' ')]

    step = request_info['root'][0].find('step')
    if step is not None:
        for k in [
            'dp_level',
            'dp_mplay',
            'enemy_damage',
            'enemy_defeat_flg',
            'mission_clear_num',
            'progress',
            'sp_level',
            'sp_mplay',
            'tips_read_list',
            'total_point',
        ]:
            game_profile['stepup_' + k] = int(step.attrib[k])

        is_track_ticket = step.find('is_track_ticket')
        if is_track_ticket is not None:
            game_profile['stepup_is_track_ticket'] = int(is_track_ticket.text)

    dj_ranks = request_info['root'][0].findall('dj_rank')
    dj_ranks = [] if dj_ranks is None else dj_ranks
    for dj_rank in dj_ranks:
        style = int(dj_rank.attrib['style'])

        rank = dj_rank.find('rank')
        game_profile['dj_rank_' + ['single', 'double'][style] + '_rank'] = [int(x) for x in rank.text.split(' ')]

        point = dj_rank.find('point')
        game_profile['dj_rank_' + ['single', 'double'][style] + '_point'] = [int(x) for x in point.text.split(' ')]

    notes_radars = request_info['root'][0].findall('notes_radar')
    notes_radars = [] if notes_radars is None else notes_radars
    for notes_radar in notes_radars:
        style = int(notes_radar.attrib['style'])
        score = notes_radar.find('radar_score')
        game_profile['notes_radar_' + ['single', 'double'][style]] = [int(x) for x in score.text.split(' ')]

    achievements = request_info['root'][0].find('achievements')
    if achievements is not None:
        for k in [
            'last_weekly',
            'pack_comp',
            'pack_flg',
            'pack_id',
            'play_pack',
            'visit_flg',
            'weekly_num',
        ]:
            game_profile['achievements_' + k] = int(achievements.attrib[k])

        trophy = achievements.find('trophy')
        if trophy is not None:
            game_profile['achievements_trophy'] = [int(x) for x in trophy.text.split(' ')]

    grade = request_info['root'][0].find('grade')
    if grade is not None:
        grade_values = []
        for g in grade.findall('g'):
            grade_values.append([int(x) for x in g.text.split(' ')])

        profile['grade_single'] = int(grade.attrib['sgid'])
        profile['grade_double'] = int(grade.attrib['dgid'])
        profile['grade_values'] = grade_values

    deller_amount = game_profile.get('deller', 0)
    deller = request_info['root'][0].find('deller')
    if deller is not None:
        deller_amount = int(deller.attrib['deller'])
    game_profile['deller'] = deller_amount

    language = request_info['root'][0].find('language_setting')
    if language is not None:
        language_value = int(language.attrib['language'])
        game_profile['language_setting'] = language_value

    game_profile['spnum'] = game_profile.get('spnum', 0) + (1 if clt == 0 else 0)
    game_profile['dpnum'] = game_profile.get('dpnum', 0) + (1 if clt == 1 else 0)

    if request_info['model'] == "TDJ":
        game_profile['lightning_play_data_spnum'] = game_profile.get('lightning_play_data_spnum', 0) + (1 if clt == 0 else 0)
        game_profile['lightning_play_data_dpnum'] = game_profile.get('lightning_play_data_dpnum', 0) + (1 if clt == 1 else 0)

    profile['version'][str(game_version)] = game_profile

    get_db().table('iidx_profile').upsert(profile, where('card') == cid)

    response = E.response(
        E.IIDX29pc(
            iidxid=xid,
            cltype=clt
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/visit')
async def iidx29pc_visit(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc(
            aflg=1,
            anum=1,
            pflg=1,
            pnum=1,
            sflg=1,
            snum=1,
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/reg')
async def iidx29pc_reg(request: Request):
    request_info = await core_process_request(request)
    game_version = request_info['game_version']

    cid = request_info['root'][0].attrib['cid']
    name = request_info['root'][0].attrib['name']
    pid = request_info['root'][0].attrib['pid']

    db = get_db().table('iidx_profile')
    all_profiles_for_card = db.get(Query().card == cid)

    if all_profiles_for_card is None:
        all_profiles_for_card = {
            'card': cid,
            'version': {}
        }

    if 'iidx_id' not in all_profiles_for_card:
        iidx_id = random.randint(10000000, 99999999)
        all_profiles_for_card['iidx_id'] = iidx_id

    all_profiles_for_card['version'][str(game_version)] = {
        'game_version': game_version,
        'djname': name,
        'region': int(pid),
        'head': 0,
        'hair': 0,
        'face': 0,
        'hand': 0,
        'body': 0,
        'frame': 0,
        'turntable': 0,
        'explosion': 0,
        'bgm': 0,
        'folder_mask': 0,
        'sudden': 0,
        'judge_pos': 0,
        'categoryvoice': 0,
        'note': 0,
        'fullcombo': 0,
        'keybeam': 0,
        'judgestring': 0,
        'soundpreview': 0,
        'grapharea': 0,
        'effector_lock': 0,
        'effector_type': 0,
        'explosion_size': 0,
        'alternate_hcn': 0,
        'kokokara_start': 0,
        'd_auto_adjust': 0,
        'd_auto_scrach': 0,
        'd_camera_layout': 0,
        'd_disp_judge': 0,
        'd_exscore': 0,
        'd_gauge_disp': 0,
        'd_ghost_score': 0,
        'd_gno': 0,
        'd_graph_score': 0,
        'd_gtype': 0,
        'd_hispeed': 0.000000,
        'd_judge': 0,
        'd_judgeAdj': 0,
        'd_lane_brignt': 0,
        'd_liflen': 0,
        'd_notes': 0.000000,
        'd_opstyle': 0,
        'd_pace': 0,
        'd_sdlen': 0,
        'd_sdtype': 0,
        'd_sorttype': 0,
        'd_sub_gno': 0,
        'd_timing': 0,
        'd_tsujigiri_disp': 0,
        'd_tune': 0,
        'dach': 0,
        'dp_opt': 0,
        'dp_opt2': 0,
        'dpnum': 0,
        'gpos': 0,
        'mode': 0,
        'ngrade': 0,
        'pmode': 0,
        'rtype': 0,
        's_auto_adjust': 0,
        's_auto_scrach': 0,
        's_camera_layout': 0,
        's_disp_judge': 0,
        's_exscore': 0,
        's_gauge_disp': 0,
        's_ghost_score': 0,
        's_gno': 0,
        's_graph_score': 0,
        's_gtype': 0,
        's_hispeed': 0.000000,
        's_judge': 0,
        's_judgeAdj': 0,
        's_lane_brignt': 0,
        's_liflen': 0,
        's_notes': 0.000000,
        's_opstyle': 0,
        's_pace': 0,
        's_sdlen': 0,
        's_sdtype': 0,
        's_sorttype': 0,
        's_sub_gno': 0,
        's_timing': 0,
        's_tsujigiri_disp': 0,
        's_tune': 0,
        'sach': 0,
        'sp_opt': 0,
        'spnum': 0,
        'deller': 0,

        # Step up mode
        'stepup_dp_level': 0,
        'stepup_dp_mplay': 0,
        'stepup_enemy_damage': 0,
        'stepup_enemy_defeat_flg': 0,
        'stepup_mission_clear_num': 0,
        'stepup_progress': 0,
        'stepup_sp_level': 0,
        'stepup_sp_mplay': 0,
        'stepup_tips_read_list': 0,
        'stepup_total_point': 0,
        'stepup_is_track_ticket': 0,

        # DJ Rank
        'dj_rank_single_rank': [0] * 15,
        'dj_rank_double_rank': [0] * 15,
        'dj_rank_single_point': [0] * 15,
        'dj_rank_double_point': [0] * 15,

        # Notes Radar
        'notes_radar_single': [0] * 6,
        'notes_radar_double': [0] * 6,

        # Grades
        'grade_single': -1,
        'grade_double': -1,
        'grade_values': [],

        # Achievements
        'achievements_trophy': [0] * 160,
        'achievements_last_weekly': 0,
        'achievements_pack_comp': 0,
        'achievements_pack_flg': 0,
        'achievements_pack_id': 0,
        'achievements_play_pack': 0,
        'achievements_visit_flg': 0,
        'achievements_weekly_num': 0,

        # Other
        'language_setting': 0,
        'movie_agreement': 0,
        'lightning_play_data_spnum': 0,
        'lightning_play_data_dpnum': 0,

        # Lightning model settings
        'lightning_setting_slider': [0] * 7,
        'lightning_setting_light': [1] * 10,
        'lightning_setting_concentration': 0,
        'lightning_setting_headphone_vol': 0,
        'lightning_setting_resistance_sp_left': 0,
        'lightning_setting_resistance_sp_right': 0,
        'lightning_setting_resistance_dp_left': 0,
        'lightning_setting_resistance_dp_right': 0,
        'lightning_setting_skin_0': 0,
        'lightning_setting_flg_skin_0': 0,

        # Event_1 settings
        'event_1_story_prog': 0,
        'event_1_last_select_area': 0,
        'event_1_failed_num': 0,
        'event_1_event_play_num': 0,
        'event_1_last_select_area_id': 0,
        'event_1_last_select_platform_type': 0,
        'event_1_last_select_platform_id': 0,

        # Web UI/Other options
        '_show_category_grade': 0,
        '_show_category_status': 1,
        '_show_category_difficulty': 1,
        '_show_category_alphabet': 1,
        '_show_category_rival_play': 0,
        '_show_category_rival_winlose': 1,
        '_show_category_all_rival_play': 0,
        '_show_category_arena_winlose': 1,
        '_show_rival_shop_info': 0,
        '_hide_play_count': 0,
        '_show_score_graph_cutin': 1,
        '_hide_iidx_id': 0,
        '_classic_hispeed': 0,
        '_beginner_option_swap': 1,
        '_show_lamps_as_no_play_in_arena': 0,

        'skin_customize_flag_frame': 0,
        'skin_customize_flag_bgm': 0,
        'skin_customize_flag_lane': 0
    }
    db.upsert(all_profiles_for_card, where('card') == cid)

    card, card_split = get_id_from_profile(cid)

    response = E.response(
        E.IIDX29pc(
            id=card,
            id_str=card_split
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/getLaneGachaTicket')
async def iidx29pc_getlanegachaticket(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc(
            E.ticket(
                ticket_id=0,
                arrange_id=0,
                expire_date=0,
            ),
            E.setting(
                sp=0,
                dp_left=0,
                dp_right=0,
            ),
            E.info(
                last_page=0,
            ),
            E.free(
                num=10,
            ),
            E.favorite(
                arrange=0,
            ),
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post('/{gameinfo}/IIDX29pc/drawLaneGacha')
async def iidx29pc_drawlanegacha(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc(
            E.ticket(
                ticket_id=0,
                arrange_id=0,
                expire_date=0,
            ),
            E.session(
                session_id=0
            ),
            status=0
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)

@router.post('/{gameinfo}/IIDX29pc/eaappliresult')
async def iidx29pc_eaappliresult(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc()
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)

@router.post('/{gameinfo}/IIDX29pc/logout')
async def iidx29pc_logout(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.IIDX29pc()
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)
