#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

struct Menu {
    char name[30];
    int price;
    int qty;
};

int main()
{
    //ID와 PW입력
    char user_name[20];
    char user_id[20];
    char user_pw[] = "1234";
    char check_pw[20];
    int login_cnt = 0;  // 로그인 횟수 저장

    printf("사용자의 이름을 입력하세요 : ");
    scanf("%s", user_name);
    getchar();
    printf("개인정보(ID)를 입력하세요 : ");
    scanf("%s", user_id);
    printf("사용자의 이름은 %s 입니다\n", user_name);
    printf("사용자의 개인정보(ID)는 %s 입니다\n", user_id);

    while (login_cnt < 3)
    {
        printf("\n암호를 입력하세요 (%d/3회 시도): ", login_cnt + 1);
        scanf("%s", check_pw);

        if (strcmp(user_pw, check_pw) == 0)
        {
            printf("\n어서오세요! 두정 기사식당 입니다.\n");
            break;
        }
        else
        {
            login_cnt++;
            printf("암호가 틀렸습니다. (남은 기회: %d번)\n", 3 - login_cnt);

            if (login_cnt == 3)
            {
                printf("\n암호 3회 오류! 프로그램을 강제 종료합니다.\n");
                return 1; // 프로그램 즉시 종료
            }
        }
    }

    //메뉴 화면
    struct Menu rice[5] = 
    {
    {"오므라이스",8000,0}, {"백반",6500,0}, {"볶음밥",7500,0}, {"카레라이스",7000,0}, {"비빔밥",7000,0}
    };

    struct Menu soup[5] = 
    {
        {"미역국", 5000,0}, {"황태국",5500,0}, {"된장국",5000,0}, {"소고기무국",6000,0}, {"시래기국",5000,0}
    };

    struct Menu side[9] = 
    {
        {"돈까스",8000,0}, {"멧돼지고기",12000,0}, {"돼지고기두루치기",10000,0}, {"돼지고기 수육",11000,0},
        {"소고기",16000,0}, {"달걀프라이",1000,0}, {"오징어",8000,0}, {"콩나물",1000,0}, {"김치",500,0}
    };

    struct Menu drink[7] = 
    {
        {"사케",8000,0}, {"생맥주",5000,0}, {"하이볼",7000,0}, {"소주",4000,0},{"카스",4000,0}, 
        {"하이트",4000,0}, {"소맥",5500,0}
    };

    int choice = 0;
    int rice_choice, soup_choice, side_choice, drink_choice;
    int rice_cnt = 0, soup_cnt = 0, side_cnt = 0, drink_cnt = 0;
    int birth;
    int total_revenue = 0, vistor_cnt = 0;

    while (1)
    {
        printf("\n****************************************\n");
        printf("          두정 기사식당 메뉴판            \n");
        printf("****************************************\n");
        printf("1. 밥 종류 선택\n");
        printf("2. 국 종류 선택\n");
        printf("3. 반찬 종류 선택 \n");
        printf("4. 술 종류 선택\n");
        printf("5. 메뉴 선택 완료(장바구니로 이동)\n");
        printf("6. 영업 종료 및 매출 확인\n");
        printf("****************************************\n");
        printf("종류를 선택하세요 : ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1: //밥
            printf("\n밥 종류를 선택하셨습니다.\n");
            printf("*********************\n");
            printf("       밥 종류        \n");
            printf("*********************\n");
            for (int i = 0; i < 5; i++)
            {
                printf("%d. %-10s %d원\n", i + 1, rice[i].name, rice[i].price);
            }
            printf("0. 선택 완료\n");
            printf("*********************\n");
            while (1)
            {
                printf("메뉴를 선택하세요 : ");
                scanf("%d", &rice_choice);

                if (rice_choice == 0)
                {
                    printf("밥 선택을 종료합니다.\n");
                    break;
                }
                else if (rice_cnt >= 2)
                {
                    printf("배터져요! 밥은 2종류까지만 선택 가능합니다.\n");
                    printf("\n");
                }
                else if (rice_choice >= 1 && rice_choice <= 5)
                {
                    rice[rice_choice - 1].qty++; // 장바구니에 저장
                    rice_cnt++;
                    printf("> %s 담기 완료!\n", rice[rice_choice - 1].name);
                    printf("\n");
                }
                else
                {
                    printf("잘못된 번호입니다. 다시 입력해주세요.\n");
                }
            }
            break;

        case 2: //국
            printf("\n국 종류를 선택하셨습니다.\n");
            printf("*********************\n");
            printf("       국 종류        \n");
            printf("*********************\n");
            for (int i = 0; i < 5; i++)
            {
                printf("%d. %-10s %d원\n", i + 1, soup[i].name, soup[i].price);
            }
            printf("0. 선택 완료\n");
            printf("*********************\n");
            while (1)
            {
                printf("메뉴를 선택하세요 : ");
                scanf("%d", &soup_choice);

                if (soup_choice == 0)
                {
                    printf("> 국 선택을 종료합니다.\n");
                    break;
                }
                else if (soup_cnt >= 3)
                {
                    printf("국이 너무 많습니다. 국은 총 3그릇까지만 선택 가능합니다.\n");
                    printf("\n");
                }
                else if (soup_choice >= 1 && soup_choice <= 5)
                {
                    soup[soup_choice - 1].qty++;
                    soup_cnt++;
                    printf("> %s 담기 완료!\n", soup[soup_choice - 1].name);
                    printf("\n");
                }
                else
                {
                    printf("잘못된 번호입니다. 다시 입력해주세요.\n");
                }
            }
            break;

        case 3: //반찬
            printf("\n반찬 종류를 선택하셨습니다.\n");
            printf("*****************************\n");
            printf("          반찬 종류         \n");
            printf("*****************************\n");
            for (int i = 0; i < 9; i++)
            {
                printf("%d. %-17s %5d원\n", i + 1, side[i].name, side[i].price);
            }
            printf("0. 선택 완료\n");
            printf("***************************\n");
            while (1)
            {
                printf("메뉴를 선택하세요 : ");
                scanf("%d", &side_choice);

                if (side_choice == 0)
                {
                    printf("> 반찬 선택을 종료합니다.\n");
                    break;
                }
                else if (side_choice >= 1 && side_choice <= 9)
                {

                    side[side_choice - 1].qty++;
                    side_cnt++;
                    printf("> %s 담기 완료!\n", side[side_choice - 1].name);
                    printf("\n");
                }
                else
                {
                    printf("잘못된 번호입니다. 다시 입력해주세요.\n");
                }
            }
            break;
        case 4:
            printf("\n술 종류를 선택하셨습니다.\n");
            printf("나이확인을 위해 태어난 연도를 입력해주세요 : ");
            scanf("%d", &birth);
            //printf("입력된 연도: %d\n", birth);
            if (2026 - birth < 19)
            {
                printf("미성년자한테는 술을 판매하지 않습니다.\n");
                break;
            }
            printf("*********************\n");
            printf("        술 종류        \n");
            printf("*********************\n");
            for (int i = 0; i < 7; i++)
            {
                printf("%d. %-10s %d원\n", i + 1, drink[i].name, drink[i].price);
            }
            printf("0. 선택 완료\n");
            printf("*********************\n");
            while (1)
            {
                printf("메뉴를 선택하세요 : ");
                scanf("%d", &drink_choice);

                if (drink_choice == 0)
                {
                    printf("술 선택을 종료합니다.\n");
                    break;
                }
                else if (drink_choice >= 1 && drink_choice <= 7)
                {
                    drink[drink_choice - 1].qty++;
                    drink_cnt++;
                    printf("> %s 담기 완료!\n", drink[drink_choice - 1].name);
                    printf("\n");
                }
                else
                {
                    printf("잘못된 번호입니다. 다시 입력해주세요.\n");
                }
            }
            break;
        case 5:
        {
            int cart_choice, pay;
            int rice_total = 0, soup_total = 0, side_total = 0, drink_total = 0;
            int total = 0;

            printf("\n====================    장바구니    ====================\n"); //54
            printf("%-17s\t%s\t%s\n", "메뉴명", "수량", "  금액");
            printf("--------------------------------------------------------\n");
            //-- 1. 밥 --5
            for (int i = 0; i < 5; i++) 
            {
                if (rice[i].qty > 0) // 선택된 메뉴만 출력
                { 
                    printf("%-17s\t% d\t%5d원\n", rice[i].name, rice[i].qty, rice[i].price * rice[i].qty);
                    rice_total += rice[i].price * rice[i].qty;
                }
            }
            // -- 2. 국 --
            for (int i = 0; i < 5; i++) 
            {
                if (soup[i].qty > 0) 
                {
                    printf("%-17s\t% d\t%5d원\n", soup[i].name, soup[i].qty, soup[i].price * soup[i].qty);
                    soup_total += soup[i].price * soup[i].qty;
                }
            }
            // -- 3. 반찬 --
            for (int i = 0; i < 9; i++) 
            {
                if (side[i].qty > 0) 
                {
                    printf("%-17s\t% d\t%5d원\n", side[i].name, side[i].qty, side[i].price* side[i].qty);
                    side_total += side[i].price * side[i].qty;
                }
            }
            // -- 4. 술 --
            for (int i = 0; i < 7; i++) {
                if (drink[i].qty > 0) {
                    printf("%-17s\t% d\t%5d원\n", drink[i].name, drink[i].qty, drink[i].price* drink[i].qty);
                    drink_total += drink[i].price * drink[i].qty;
                }
            }
            printf("--------------------------------------------------------\n");

            //반찬 할인 확인
            int side_type_cnt = 0;
            for (int i = 0; i < 9; i++)
            {
                if (side[i].qty > 0) 
                {
                    side_type_cnt++;
                }
            }
            if (side_type_cnt == 9)
            {
                printf("모든 반찬 선택하셨군요!! 반찬 금액 20%% 할인이 적용됩니다!\n");
                side_total = side_total * 0.8;
            }

            total = rice_total + soup_total + side_total + drink_total;
            printf("최종 결제 금액 : %d원\n", total);
            printf("========================================================\n");
            printf("1. 결제 진행  2. 주문 취소 : ");
            scanf("%d", &cart_choice);

            if (cart_choice == 2)
            {
                printf("\n모든 주문을 취소하고 처음으로 돌아갑니다.\n");
                rice_cnt = 0; soup_cnt = 0; side_cnt = 0; drink_cnt = 0;
                for (int i = 0; i < 9; i++)
                {
                    if (i < 5) 
                    {
                        rice[i].qty = 0;
                        soup[i].qty = 0;
                    }
                    if (i < 7)
                    {
                        drink[i].qty = 0;
                    }
                    side[i].qty = 0;
                }
                break;
            }

            else if (cart_choice == 1)
            {
                printf("\n결제 수단을 선택하세요 (1.카드  2.현금) : ");
                scanf("%d", &pay);

                //카드 결제 진행
                if (pay == 1)
                {
                    int card_num, confirm;
                    char card_name[20] = "";

                    printf("카드번호 4자리를 입력하세요: ");
                    scanf("%d", &card_num);

                    int card_pre = card_num / 100;

                    if (card_pre == 10) {
                        strcpy(card_name, "현대카드");
                    }
                    else if (card_pre == 20) {
                        strcpy(card_name, "삼성카드");
                    }
                    else if (card_pre == 30) {
                        strcpy(card_name, "신한카드");
                    }
                    else if (card_pre == 40) {
                        strcpy(card_name, "국민카드");
                    }
                    else {
                        printf("등록되지 않은 카드 번호입니다.\n");
                        break;
                    }
                    printf("--------------------------------------------\n");
                    printf("%s가 맞습니까?\n", card_name);
                    printf("1. 예  2. 아니요 : ");
                    scanf("%d", &confirm);

                    if (confirm == 1) {
                        printf("결제가 정상적으로 승인되었습니다!\n");
                        printf("--------------------------------------------\n");
                    }
                    else
                    {
                        printf("결제가 취소되었습니다. 메인 메뉴로 돌아갑니다.\n");
                        printf("--------------------------------------------\n");
                        break;
                    }
                }
                //현금 결제 진행
                else if (pay == 2)
                {
                    // 1. 현금 10% 추가 할인 적용
                    printf("\n현금 결제 10%% 할인이 적용됩니다!\n");
                    total = total * 0.9;
                    printf("최종 결제 금액: %d원\n", total);

                    int cash_input;
                    while (1)
                    {
                        printf("현금을 투입하세요 (금액 입력): ");
                        scanf("%d", &cash_input);

                        if (cash_input >= total)
                        {
                            printf("\n결제 완료! 잔돈은 %d원입니다.\n", cash_input - total);
                            break;
                        }
                        else
                        {
                            printf("금액이 부족합니다!(부족금액: %d원) 다시 넣어주세요.\n", total - cash_input);
                        }
                    }
                }
                else
                {
                    printf("잘못된 입력입니다.");
                    break;
            }
            
            }
            printf("\n이용해주셔서 고맙습니다. 맛있는 식사 되세요!\n");

            total_revenue += total; // 이번 손님의 결제액을 총 매출에 합산
            vistor_cnt++;        // 방문 손님 수 1명 증가

            // 다음 손님을 위해 모든 데이터 초기화
            rice_cnt = 0; soup_cnt = 0; side_cnt = 0; drink_cnt = 0;
            for (int i = 0; i < 9; i++)
            {
                if (i < 5)
                {
                    rice[i].qty = 0;
                    soup[i].qty = 0;
                }
                if (i < 7)
                {
                    drink[i].qty = 0;
                }
                side[i].qty = 0;
            }

            // 3번 반복 후 체크
            if (vistor_cnt % 3 == 0) {
                printf("\n==========================================\n");
                printf("   <중간점검> 방문 손님 : %d명\n", vistor_cnt);
                printf("   <중간점검> 누적 매출 : %d원\n", total_revenue);
                printf("==========================================\n");
            }
            break;
        }
        case 6:
            printf("\n==========================================\n");
            printf(" 영업 종료: 오늘의 최종 매출 보고서 \n");
            printf(" - 총 방문 손님 수: %d명\n", vistor_cnt);
            printf(" - 오늘 총 매출액: %d원\n", total_revenue);
            printf("==========================================\n");
            printf("프로그램을 종료합니다. 수고하셨습니다!\n");
            return 1;

        } // switch 끝
    } // while 끝
    return 0;
}
