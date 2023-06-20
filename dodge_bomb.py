import sys
import random


import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
        pg.K_UP: (0,-5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
        }


def check_bound(rect: pg.rect) -> tuple[bool, bool]: #爆弾のオブジェクトのrectの座標が画面の範囲外にならないようにする関数(5)
    """
    オブジェクトが画面内or画面外を判定し、真理値をタプルを返す関数
    引数1:こうかとんRector 爆弾Rect
    戻り値:横方向、縦方向のはみ出し判定結果(画面内:True/画面外:False)
    """

    width, height = (True, True)  # 横方向、縦方向のはみ出し判定結果を真理値で初期化する(練習4)
    if rect.left < 0 or WIDTH < rect.right:  # オブジェクトのrectの座標が画面の範囲外になっているか判定する(練習4)
        width = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # オブジェクトのrectの座標が画面の範囲外になっているか判定する(練習4)
        height = False
    return (width, height)  # 横方向、縦方向のはみ出し判定結果をタプルで返す(練習4)

def main():
    gameover = False
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_go_img = pg.image.load("ex02/fig/8.png")
    kk_go_img = pg.transform.rotozoom(kk_go_img, 0, 2)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2)
    bd_img = pg.Surface((20, 20))  # 爆弾の空オブジェクトを生成する(練習1)
    kk_rct = kk_img.get_rect()  # こうかのオブジェクトのrectを取得する(練習3)
    kk_rct.center = (900, 400)  # こうかとんのオブジェクトのrectの座標を(900, 400)に設定する(練習3)
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)  # 爆弾の空オブジェクトに赤色の円を描画する(演習1)
    (x, y) = random.randint(0, WIDTH), random.randint(0, HEIGHT)  #xとyをランダムに生成する(練習1)
    bd_rct = bd_img.get_rect()   # 爆弾の空オブジェクトを取得する(練習1)
    vx , vy = +5, +5  # xとyの移動量を設定する(練習2)
    bd_rct.center = (x, y)  # 爆弾の空オブジェクトの中心座標を(x, y)に設定する(練習1)
    bd_img.set_colorkey((0, 0, 0))  #爆弾の黒色を透明にする(練習1)
    vx , vy = +10, -10  # xとyの移動量を設定する(練習2)
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾のオブジェクトが衝突しているか判定する(練習2)(演習3)
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_go_img, (kk_rct))
            pg.display.update()
            pg.time.wait(3000)
            return

        #gameoverがFolesのときにkk_imgを表示する
        key_lst = pg.key.get_pressed()  # キー入力の取得(練習3)
        sum_mv = [0, 0] # 移動量のリストを初期化する(練習3)
        for k, mv in delta.items():  # キー入力の処理(練習3)
            if key_lst[k]:
                sum_mv[0] += mv[0] # 移動量を加算する(練習3)
                sum_mv[1] += mv[1] # 移動量を加算する(練習3)
        kk_rct.move_ip(sum_mv)  # こうかのオブジェクトのrectを移動する(練習3)
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, (kk_rct))
        #screen.blit(kk_img, (kk_rct))
        bd_rct.move_ip(vx, vy)  # 爆弾のオブジェクトのrectを移動する(練習2)
        screen.blit(bd_img, (bd_rct))  # 爆弾画像をテスト描画(練習1)
        if check_bound(kk_rct) != (True, True):  # 爆弾のオブジェクトのrectの座標が画面の範囲外になっているか判定する(練習4)
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # こうかのオブジェクトのrectを移動する(練習4)    
        width, height = check_bound(bd_rct)  # 爆弾のオブジェクトのrectの座標が画面の範囲外になっているか判定する(練習4)
        if not width:
            vx = -vx
        if not height:
            vy = -vy
        # 10回爆弾の移動量を加速する(演習2)
        if tmr % 10 == 0 and tmr < 1000:
            if vx > 0:
                vx += 1
            else:
                vx -= 1
            if vy > 0:
                vy += 1
            else:
                vy -= 1
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()