# 수정된 app_eda.py 파일의 일부: EDA 클래스 내 '인구 분석' 탭 추가
# 기존 코드 아래에 추가되도록 구성

class EDA:
    def __init__(self):
        st.title("📊 Bike Sharing Demand EDA & Population Analysis")

        tabs = st.tabs([
            "Bike Sharing EDA",
            "Population Analysis"
        ])

        with tabs[0]:
            self.bike_sharing_eda()

        with tabs[1]:
            self.population_analysis()

    def bike_sharing_eda(self):
        # 기존 Bike Sharing 분석 코드 그대로 복사
        st.info("기존 Bike Sharing 분석 내용 포함 (생략)")

    def population_analysis(self):
        st.header("📈 인구 데이터 분석")

        uploaded = st.file_uploader("population_trends.csv 파일 업로드", type="csv")
        if uploaded is None:
            st.warning("CSV 파일을 업로드해주세요.")
            return

        df = pd.read_csv(uploaded)
        df.replace('-', 0, inplace=True)
        df[['인구', '출생아수(명)', '사망자수(명)']] = df[['인구', '출생아수(명)', '사망자수(명)']].apply(pd.to_numeric)

        tabs = st.tabs(["기초 통계", "연도별 추이", "지역별 분석", "변화량 분석", "시각화"])

        with tabs[0]:
            st.subheader("📋 데이터 정보")
            st.dataframe(df.head())
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
            st.dataframe(df.describe())

        with tabs[1]:
            st.subheader("📊 연도별 전국 인구 추이")
            df_national = df[df['지역'] == '전국']
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df_national, x='연도', y='인구', marker='o')
            plt.title('Population Trend by Year')
            plt.xlabel('Year')
            plt.ylabel('Population')

            # 간단 예측
            recent = df_national[df_national['연도'] >= df_national['연도'].max() - 2]
            avg_delta = (recent['출생아수(명)'] - recent['사망자수(명)']).mean()
            future_pop = df_national['인구'].iloc[-1] + avg_delta * (2035 - df_national['연도'].max())
            plt.axhline(future_pop, color='red', linestyle='--', label=f'Predicted 2035: {int(future_pop):,}')
            plt.legend()
            st.pyplot(plt)

        with tabs[2]:
            st.subheader("📌 최근 5년 지역별 인구 변화량 순위")
            year_max = df['연도'].max()
            df_recent = df[df['연도'].between(year_max - 5, year_max)]
            pop_change = df_recent.groupby('지역')['인구'].agg(['first', 'last'])
            pop_change['변화량'] = pop_change['last'] - pop_change['first']
            pop_change = pop_change.drop(index='전국').sort_values(by='변화량', ascending=False)
            plt.figure(figsize=(10, 8))
            sns.barplot(y=pop_change.index, x=pop_change['변화량'] / 1000, orient='h')
            plt.title('Population Change (5 years, unit: 1000)')
            plt.xlabel('Change (Thousands)')
            st.pyplot(plt)

        with tabs[3]:
            st.subheader("📈 인구 증감 상위 사례")
            df_pivot = df.pivot(index='연도', columns='지역', values='인구')
            df_diff = df_pivot.diff().dropna()
            top_changes = df_diff.stack().reset_index()
            top_changes.columns = ['연도', '지역', '증감']
            top100 = top_changes[top_changes['지역'] != '전국'].sort_values(by='증감', ascending=False).head(100)
            st.dataframe(top100.style.background_gradient(subset='증감', cmap='RdBu', axis=0))

        with tabs[4]:
            st.subheader("🌐 누적 인구 영역 그래프")
            df_plot = df[df['지역'] != '전국'].pivot(index='연도', columns='지역', values='인구')
            df_plot.fillna(0, inplace=True)
            df_plot = df_plot / 1000  # 단위 변환
            df_plot.plot.area(figsize=(12, 6), colormap='tab20')
            plt.title('Population by Region (Thousands)')
            plt.xlabel('Year')
            plt.ylabel('Population (Thousands)')
            st.pyplot(plt)

# 나머지 네비게이션, 페이지 정의 코드는 기존 그대로 유지
