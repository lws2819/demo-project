
import json
import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="예산 맞춤 음식 룰렛",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 예산 맞춤 음식 룰렛")
st.write("예산에 맞는 음식과 브랜드, 주변 음식점을 골라 보세요!")

# 음식 이름별 브랜드 목록
# 외부 API 없이 사용할 수 있도록 미리 등록해 둡니다.
FOOD_BRANDS = {
    "피자": ["도미노피자", "피자헛", "파파존스", "미스터피자", "피자스쿨"],
    "치킨": ["BBQ", "bhc", "교촌치킨", "굽네치킨", "푸라닭", "노랑통닭"],
    "라면": ["농심", "오뚜기", "삼양식품", "팔도"],
    "햄버거": ["맥도날드", "롯데리아", "버거킹", "맘스터치", "KFC"],
    "초밥": ["스시로", "갓덴스시", "쿠우쿠우"],
    "파스타": ["롤링파스타", "라그릴리아", "매드포갈릭"],
    "만두": ["비비고", "개성", "동원"],
    "카레": ["오뚜기", "청정원", "코코이찌방야"],
    "떡볶이": ["엽기떡볶이", "신전떡볶이", "죠스떡볶이", "청년다방"],
    "짜장면": ["홍콩반점0410", "이비가짬뽕"],
    "돈가스": ["유미카츠", "긴자료코", "아비꼬"],
    "김치찌개": ["백채김치찌개", "김치옥"],
    "김밥": ["김가네", "고봉민김밥인", "바르다김선생", "김밥천국"],
    "비빔밥": ["본죽&비빔밥", "전주비빔밥 전문점"],
    "불고기": ["한촌설렁탕", "불고기브라더스"],
    "삼겹살": ["하남돼지집", "고기싸롱", "명륜진사갈비"],
    "갈비": ["명륜진사갈비", "송추가마골"],
    "냉면": ["함흥냉면 전문점", "평양냉면 전문점"],
    "칼국수": ["명동교자", "등촌샤브칼국수"],
    "김치볶음밥": ["한솥도시락", "김밥천국"],
    "볶음밥": ["홍콩반점0410", "김밥천국"],
    "순대": ["신의주찹쌀순대", "병천순대 전문점"],
    "족발": ["가장맛있는족발", "원할머니보쌈족발"],
    "보쌈": ["원할머니보쌈족발", "놀부보쌈"],
    "우동": ["역전우동0410", "겐로쿠우동"],
    "쌀국수": ["포메인", "에머이", "미분당"],
    "샌드위치": ["써브웨이", "퀴즈노스"],
    "샐러드": ["샐러디", "포케올데이"],
    "마라탕": ["탕화쿵푸마라탕", "라화쿵부"],
    "마라샹궈": ["탕화쿵푸마라탕", "라화쿵부"],
    "부대찌개": ["놀부부대찌개", "킹콩부대찌개"],
    "된장찌개": ["한솥도시락", "한식 전문점"],
    "순두부찌개": ["북창동순두부", "한식 전문점"],
    "갈비탕": ["본설렁탕", "한식 전문점"],
    "설렁탕": ["신선설농탕", "한촌설렁탕"],
    "국밥": ["더진국", "국밥 전문점"],
    "김치전": ["한식 전문점", "전 전문점"],
    "해물파전": ["한식 전문점", "전 전문점"],
    "토스트": ["이삭토스트", "에그드랍"],
    "핫도그": ["명랑핫도그", "아리랑핫도그"],
    "떡국": ["한식 전문점"],
    "수제비": ["한식 전문점", "수제비 전문점"],
    "닭갈비": ["유가네닭갈비", "춘천닭갈비 전문점"],
    "찜닭": ["두찜", "봉추찜닭"],
    "닭강정": ["가마로강정", "인생닭강정"],
    "곱창": ["대한곱창", "곱창 전문점"],
    "막창": ["막창도둑", "막창 전문점"],
    "대창": ["대한곱창", "곱창 전문점"],
    "회": ["회 전문점", "수산시장 횟집"],
    "돈부리": ["홍대개미", "일식 전문점"],
    "오므라이스": ["오므토토마토", "양식 전문점"],
    "카레라이스": ["오뚜기", "코코이찌방야"],
    "리조또": ["양식 전문점", "파스타 전문점"],
    "스테이크": ["아웃백", "빕스", "텍사스로드하우스"],
    "주먹밥": ["봉구스밥버거", "분식 전문점"],
    "유부초밥": ["유부초밥 전문점", "분식 전문점"],
    "붕어빵": ["동네 붕어빵 가게"],
    "호떡": ["동네 호떡 가게"],
    "와플": ["와플대학", "카페"],
    "아이스크림": ["배스킨라빈스", "설빙"],
    "제육볶음": ["한솥도시락", "한식 전문점"],
    "감자탕": ["이바돔감자탕", "뼈해장국 전문점"],
    "아구찜": ["인생아구찜", "아귀찜 전문점"],
    "갈비찜": ["한식 전문점"],
    "떡갈비": ["한식 전문점"],
    "김치말이국수": ["국수 전문점"],
    "잔치국수": ["국수나무", "국수 전문점"],
    "비빔국수": ["국수나무", "국수 전문점"],
    "콩국수": ["국수 전문점"],
    "물회": ["물회 전문점"],
    "육회": ["육회바른연어", "육회 전문점"],
    "파전": ["한식 전문점", "전 전문점"],
    "전": ["전 전문점"],
    "피자빵": ["베이커리"],
    "김밥천국 김밥": ["김밥천국"]
}

# 공백, 이모지, 기호를 제거하여 음식 이름을 비교합니다.
def normalize_food_name(name):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", name).casefold()


# 기본 음식과 예상 가격
DEFAULT_CATALOG = {
    "🍕 피자": 15000,
    "🍗 치킨": 20000,
    "🍜 라면": 5000,
    "🍔 햄버거": 8000,
    "🍣 초밥": 18000,
    "🍝 파스타": 14000,
    "🥟 만두": 8000,
    "🍛 카레": 9000,
    "🌶️ 떡볶이": 7000,
    "🍜 짜장면": 8000,
    "🍱 돈가스": 11000,
    "🍲 김치찌개": 10000
}

if "catalog" not in st.session_state:
    st.session_state.catalog = {
        name: {
            "price": price,
            "brands": FOOD_BRANDS.get(
                normalize_food_name(name), []
            ).copy()
        }
        for name, price in DEFAULT_CATALOG.items()
    }

catalog = st.session_state.catalog

st.subheader("💰 1. 예산 설정")

budget = st.number_input(
    "사용할 예산 (원)",
    min_value=0,
    max_value=1000000,
    value=15000,
    step=1000
)

st.caption("가격은 예시이며 실제 매장 가격과 다를 수 있습니다.")

st.divider()
st.subheader("📍 2. 주변 음식점 입력")

st.write(
    "가까운 음식점 이름을 쉼표 또는 줄바꿈으로 구분해 입력하세요. "
    "입력한 음식점도 브랜드 룰렛에 추가됩니다."
)

nearby_text = st.text_area(
    "주변 음식점 이름",
    placeholder="예: 우리 동네 김밥집, OO분식, OO중국집",
    key="nearby_restaurants",
    height=90
)

nearby_places = [
    place.strip()
    for place in re.split(r"[,，\n]", nearby_text)
    if place.strip()
]

if nearby_places:
    st.success(f"주변 음식점 {len(nearby_places)}개를 룰렛에 추가합니다.")
else:
    st.info(
        "음식점 이름을 입력하지 않으면 "
        "'주변 음식점 (직접 확인)' 항목이 룰렛에 포함됩니다."
    )

st.divider()
st.subheader("🍽️ 3. 음식 추가 및 관리")

with st.form("add_food_form", clear_on_submit=True):
    new_food = st.text_input(
        "추가할 음식 이름",
        placeholder="예: 김밥"
    )
    new_price = st.number_input(
        "예상 가격 (원)",
        min_value=0,
        max_value=1000000,
        value=5000,
        step=500
    )
    add_clicked = st.form_submit_button("➕ 음식 추가")

if add_clicked:
    food_name = new_food.strip()
    normalized = normalize_food_name(food_name)

    known_foods = {
        normalize_food_name(name): name
        for name in FOOD_BRANDS
    }

    registered_foods = {
        normalize_food_name(name)
        for name in catalog
    }

    if not normalized:
        st.error("음식 이름을 입력해 주세요.")
    elif normalized not in known_foods:
        st.error(
            "브랜드 정보가 등록된 음식 목록에서 찾을 수 없습니다. "
            "현재는 미리 등록된 음식만 추가할 수 있습니다."
        )
    elif normalized in registered_foods:
        st.warning("이미 등록된 음식입니다.")
    else:
        canonical_name = known_foods[normalized]
        catalog[food_name] = {
            "price": int(new_price),
            "brands": FOOD_BRANDS[canonical_name].copy()
        }
        st.success(
            f"{food_name} 추가 완료! "
            f"브랜드 {len(catalog[food_name]['brands'])}개를 연결했습니다."
        )
        st.rerun()

if catalog:
    st.caption(f"등록된 음식: {len(catalog)}개")

    names = list(catalog.keys())
    columns = st.columns(2)

    for i, name in enumerate(names):
        with columns[i % 2]:
            left, right = st.columns([5, 1])
            left.write(f"**{name}**")
            left.caption(f"예상 가격: {catalog[name]['price']:,}원")
            left.caption(
                f"연결된 브랜드: {len(catalog[name]['brands'])}개"
            )

            if right.button("❌", key=f"delete_{i}"):
                del catalog[name]
                st.rerun()

st.divider()
st.subheader("🎡 4. 예산에 맞는 음식 추천")

affordable = [
    {
        "name": name,
        "price": item["price"],
        "brands": item["brands"]
    }
    for name, item in catalog.items()
    if item["price"] <= budget
]

if not affordable:
    st.warning(
        "예산에 맞는 음식이 없습니다. 예산을 높이거나 "
        "음식의 예상 가격을 조정해 주세요."
    )
else:
    st.success(f"예산에 맞는 음식 {len(affordable)}개를 찾았습니다.")

    columns = st.columns(3)
    for i, item in enumerate(affordable):
        with columns[i % 3]:
            st.write(item["name"])
            st.caption(f"{item['price']:,}원")

    st.divider()
    st.subheader("🎯 5. 음식 및 브랜드 룰렛")

    wheel_data = json.dumps(
        affordable,
        ensure_ascii=False
    ).replace("</", "<\\/")

    nearby_json = json.dumps(
        nearby_places,
        ensure_ascii=False
    ).replace("</", "<\\/")

    wheel_html = r"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            padding: 12px 8px 25px;
            font-family: Arial, sans-serif;
            text-align: center;
            background: transparent;
        }

        h2 { font-size: 25px; margin: 10px 0; }

        #stageInfo {
            color: #666;
            font-size: 16px;
            margin: 8px 0 15px;
        }

        .wheel-area {
            position: relative;
            width: min(88vw, 540px);
            margin: 0 auto;
        }

        canvas {
            display: block;
            width: 100%;
            height: auto;
        }

        .pointer {
            position: absolute;
            top: -2px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 2;
            width: 0;
            height: 0;
            border-left: 19px solid transparent;
            border-right: 19px solid transparent;
            border-top: 38px solid #2d3436;
        }

        button { font-family: inherit; }

        .main-button {
            margin: 18px 5px 8px;
            padding: 15px 25px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: #6c5ce7;
            border: none;
            border-radius: 13px;
            cursor: pointer;
        }

        .main-button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        #brandButton {
            display: none;
            background: #00a884;
        }

        #resetButton {
            display: none;
            background: #eeeeee;
            color: #333;
        }

        #popupOverlay {
            position: fixed;
            inset: 0;
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
            background: rgba(0, 0, 0, 0.62);
        }

        #popupOverlay.show { display: flex; }

        .popup {
            position: relative;
            width: min(94vw, 600px);
            padding: 38px 22px 28px;
            background: white;
            border-radius: 25px;
            box-shadow: 0 14px 50px rgba(0, 0, 0, 0.3);
            animation: popIn 0.25s ease-out;
        }

        @keyframes popIn {
            from { opacity: 0; transform: scale(0.75); }
            to { opacity: 1; transform: scale(1); }
        }

        #closeButton {
            position: absolute;
            top: 10px;
            right: 12px;
            width: 42px;
            height: 42px;
            border: none;
            border-radius: 50%;
            background: #f1f2f6;
            font-size: 28px;
            cursor: pointer;
        }

        .result-title {
            margin: 5px 0 18px;
            color: #6c5ce7;
            font-size: clamp(22px, 5vw, 31px);
            font-weight: bold;
        }

        #resultFood {
            overflow-wrap: anywhere;
            margin: 12px 0 18px;
            font-size: clamp(34px, 8vw, 60px);
            font-weight: 800;
            line-height: 1.3;
            color: #222;
        }

        #resultDetail {
            color: #555;
            font-size: 18px;
            margin: 8px 0;
        }

        #timerText {
            margin-top: 20px;
            color: #888;
            font-size: 14px;
        }
    </style>
    </head>
    <body>
        <h2 id="wheelTitle">🍽️ 음식 룰렛</h2>
        <div id="stageInfo">예산에 맞는 음식 중 하나를 골라요!</div>

        <div class="wheel-area">
            <div class="pointer"></div>
            <canvas id="wheel" width="700" height="700"></canvas>
        </div>

        <button id="spinButton" class="main-button" onclick="spinWheel()">
            🎯 음식 룰렛 돌리기
        </button>
        <br>
        <button id="brandButton" class="main-button" onclick="startBrandWheel()">
            🏷️ 브랜드 룰렛 돌리기
        </button>
        <button id="resetButton" class="main-button" onclick="resetFoodWheel()">
            ↩ 음식 다시 고르기
        </button>

        <div id="popupOverlay">
            <div class="popup" role="dialog" aria-modal="true">
                <button id="closeButton" aria-label="닫기" onclick="closePopup()">×</button>
                <div id="resultTitle" class="result-title">🎉 결과 발표! 🎉</div>
                <div id="resultFood"></div>
                <div id="resultDetail"></div>
                <div id="timerText">이 창은 3초 후 자동으로 닫힙니다.</div>
            </div>
        </div>

        <script>
            const foodData = __FOOD_DATA__;
            const nearbyPlaces = __NEARBY_DATA__;

            const colors = [
                "#FF7675", "#74B9FF", "#55EFC4", "#FFEAA7",
                "#A29BFE", "#FAB1A0", "#81ECEC", "#FD79A8",
                "#FDCB6E", "#B8E994", "#82CCDD", "#D6A2E8"
            ];

            const canvas = document.getElementById("wheel");
            const ctx = canvas.getContext("2d");
            const spinButton = document.getElementById("spinButton");
            const brandButton = document.getElementById("brandButton");
            const resetButton = document.getElementById("resetButton");
            const overlay = document.getElementById("popupOverlay");

            const center = canvas.width / 2;
            const radius = center - 12;
            const tau = Math.PI * 2;

            let options = foodData.map(item => item.name);
            let rotation = 0;
            let spinning = false;
            let stage = "food";
            let selectedFood = null;
            let closeTimer = null;

            function normalizeAngle(angle) {
                return ((angle % tau) + tau) % tau;
            }

            function drawWheel() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                if (options.length === 0) return;

                const arc = tau / options.length;

                ctx.save();
                ctx.translate(center, center);
                ctx.rotate(rotation);

                for (let i = 0; i < options.length; i++) {
                    const start = -Math.PI / 2 + i * arc;
                    const end = start + arc;

                    ctx.beginPath();
                    ctx.moveTo(0, 0);
                    ctx.arc(0, 0, radius, start, end);
                    ctx.closePath();

                    ctx.fillStyle = colors[i % colors.length];
                    ctx.fill();
                    ctx.strokeStyle = "#fff";
                    ctx.lineWidth = 4;
                    ctx.stroke();

                    ctx.save();
                    ctx.rotate(start + arc / 2);
                    ctx.textAlign = "right";
                    ctx.textBaseline = "middle";
                    ctx.fillStyle = "#222";
                    ctx.font = options.length > 12
                        ? "bold 18px Arial"
                        : "bold 23px Arial";

                    let label = options[i];
                    const maxLength = options.length > 12 ? 9 : 13;

                    if (label.length > maxLength) {
                        label = label.slice(0, maxLength - 1) + "…";
                    }

                    ctx.fillText(label, radius - 24, 0);
                    ctx.restore();
                }

                ctx.beginPath();
                ctx.arc(0, 0, 35, 0, tau);
                ctx.fillStyle = "#fff";
                ctx.fill();
                ctx.strokeStyle = "#333";
                ctx.lineWidth = 4;
                ctx.stroke();

                ctx.fillStyle = "#6c5ce7";
                ctx.font = "bold 22px Arial";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText("GO", 0, 0);

                ctx.restore();
            }

            function getPointerIndex() {
                const arc = tau / options.length;
                return Math.floor(normalizeAngle(-rotation) / arc)
                    % options.length;
            }

            function closePopup() {
                overlay.classList.remove("show");

                if (closeTimer !== null) {
                    clearTimeout(closeTimer);
                    closeTimer = null;
                }
            }

            function showPopup(title, result, detail) {
                document.getElementById("resultTitle").textContent = title;
                document.getElementById("resultFood").textContent = result;
                document.getElementById("resultDetail").textContent = detail;
                overlay.classList.add("show");

                if (closeTimer !== null) clearTimeout(closeTimer);

                closeTimer = setTimeout(() => {
                    overlay.classList.remove("show");
                    closeTimer = null;
                }, 3000);
            }

            function spinWheel() {
                if (spinning || options.length === 0) return;

                closePopup();
                spinning = true;
                spinButton.disabled = true;
                brandButton.disabled = true;
                spinButton.textContent = "🎡 돌리는 중...";

                const targetIndex = Math.floor(Math.random() * options.length);
                const arc = tau / options.length;
                const targetCenter = (targetIndex + 0.5) * arc;
                const desiredRotation = normalizeAngle(-targetCenter);
                const currentRotation = normalizeAngle(rotation);
                const correction = normalizeAngle(
                    desiredRotation - currentRotation
                );

                const fullTurns = 5 + Math.floor(Math.random() * 3);
                const startRotation = rotation;
                const targetRotation =
                    startRotation + fullTurns * tau + correction;

                const change = targetRotation - startRotation;
                const duration = 4500 + Math.random() * 700;
                const startTime = performance.now();

                function animate(now) {
                    const progress = Math.min(
                        (now - startTime) / duration, 1
                    );
                    const eased = 1 - Math.pow(1 - progress, 4);

                    rotation = startRotation + change * eased;
                    drawWheel();

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    } else {
                        rotation = normalizeAngle(targetRotation);
                        drawWheel();

                        const result = options[getPointerIndex()];

                        spinning = false;
                        spinButton.disabled = false;
                        brandButton.disabled = false;

                        if (stage === "food") {
                            selectedFood = foodData.find(
                                item => item.name === result
                            );

                            spinButton.textContent = "🎯 음식 다시 뽑기";
                            brandButton.style.display = "inline-block";
                            resetButton.style.display = "inline-block";

                            showPopup(
                                "🎉 오늘의 음식은?",
                                result,
                                "예상 가격: " +
                                selectedFood.price.toLocaleString() + "원"
                            );
                        } else {
                            spinButton.textContent = "🏷️ 브랜드 다시 뽑기";

                            showPopup(
                                "🎉 추천 브랜드 또는 음식점은?",
                                result,
                                "선택한 음식: " + selectedFood.name
                            );
                        }
                    }
                }

                requestAnimationFrame(animate);
            }

            function startBrandWheel() {
                if (spinning || !selectedFood) return;

                closePopup();

                // 음식에 맞는 브랜드 + 주변 음식점 이름을 함께 추가합니다.
                const brandOptions = selectedFood.brands.slice();

                for (const place of nearbyPlaces) {
                    if (!brandOptions.includes(place)) {
                        brandOptions.push(place);
                    }
                }

                const genericNearby = "주변 음식점 (직접 확인)";
                if (!brandOptions.includes(genericNearby)) {
                    brandOptions.push(genericNearby);
                }

                options = brandOptions;
                rotation = 0;
                stage = "brand";

                document.getElementById("wheelTitle").textContent =
                    "🏷️ 브랜드 및 주변 음식점 룰렛";

                document.getElementById("stageInfo").textContent =
                    selectedFood.name +
                    " 관련 브랜드와 주변 음식점 중 하나를 골라요!";

                spinButton.textContent = "🏷️ 브랜드 룰렛 돌리기";
                brandButton.style.display = "none";

                drawWheel();
            }

            function resetFoodWheel() {
                if (spinning) return;

                closePopup();
                options = foodData.map(item => item.name);
                rotation = 0;
                stage = "food";
                selectedFood = null;

                document.getElementById("wheelTitle").textContent =
                    "🍽️ 음식 룰렛";

                document.getElementById("stageInfo").textContent =
                    "예산에 맞는 음식 중 하나를 골라요!";

                spinButton.textContent = "🎯 음식 룰렛 돌리기";
                brandButton.style.display = "none";
                resetButton.style.display = "none";

                drawWheel();
            }

            document.addEventListener("keydown", event => {
                if (event.key === "Escape") closePopup();
            });

            drawWheel();
        </script>
    </body>
    </html>
    """

    wheel_html = (
        wheel_html
        .replace("__FOOD_DATA__", wheel_data)
        .replace("__NEARBY_DATA__", nearby_json)
    )

    components.html(
        wheel_html,
        height=950,
        scrolling=False
    )
