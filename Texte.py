import pygame

class texte:
    def __init__(self, fensterbreite: int, schrift = None, abstand_oben = 20):
        self.fensterbreite = fensterbreite
        self.schrift = schrift or pygame.font.Font(None, 40)
        self.abstand_oben = abstand_oben

        self.box_hoehe = 60
        self.orange_breite_links = 150
        self.orange_breite_rechts = 90

        self.box_links  = pygame.Rect(20, abstand_oben, 420, self.box_hoehe)
        self.box_rechts = pygame.Rect(fensterbreite - 20 - 340, abstand_oben, 340, self.box_hoehe)

        self.farbe_hintergrund = (240, 240, 255)
        self.farbe_rand = (170, 190, 220)
        self.farbe_text = (0, 0, 0)
        self.farbe_orange = (255, 140, 0)
        self.farbe_orange_text = (255, 255, 255)

    def _zeichne_box(self, screen, box_rect, titel, wert, orange_breite):
        radius = 8

        pygame.draw.rect(screen, self.farbe_hintergrund, box_rect, border_radius = radius)
        pygame.draw.rect(screen, self.farbe_rand, box_rect, width=3, border_radius = radius)

        wert_text = self.schrift.render(str(wert), True, self.farbe_orange_text)
        wert_rect = pygame.Rect(
            box_rect.right - orange_breite - 8,
            box_rect.y + 5,
            orange_breite,
            box_rect.height - 10
        )
        pygame.draw.rect(screen, self.farbe_orange, wert_rect, border_radius=radius - 2)

        screen.blit(
            wert_text,
            (wert_rect.centerx - wert_text.get_width() // 2,
             wert_rect.centery - wert_text.get_height() // 2)
        )

        titel_text = self.schrift.render(str(titel), True, self.farbe_text)
        max_breite = box_rect.width - orange_breite - 30

        if titel_text.get_width() > max_breite:
            text = str(titel)
            while text and self.schrift.size(text + "...")[0] > max_breite:
                text = text[:-1]
            titel_text = self.schrift.render(text + "...", True, self.farbe_text)

        screen.blit(
            titel_text,
            (box_rect.x + 12, box_rect.y + (box_rect.height - titel_text.get_height()) // 2)
        )

    def zeichne(self, screen, restzeit: int, aktiver_sektor: int, sektornamen=None):
        if sektornamen and 0 <= aktiver_sektor < len(sektornamen):
            gefahrenname = sektornamen[aktiver_sektor]
        else:
            gefahrenname = aktiver_sektor + 1

        self._zeichne_box(
            screen,
            self.box_links,
            "Aktive Gefahr",
            gefahrenname,
            self.orange_breite_links
        )

        self._zeichne_box(
            screen,
            self.box_rechts,
            "Countdown",
            f"{int(restzeit)}s",
            self.orange_breite_rechts
        )