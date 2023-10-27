% Sub-panel(s) for computational figure on track density
clf;


% define data location
DRV = 'F:\';
TRK_INPUT_Folder = '' ;



% Define Bundle Density Data
Den_tot = [];
Den_tmp = [];
Den_reg = [];


fig1 = figure(1);
set(fig1,'PaperUnits','inches','PaperSize',[8.5,11],'PaperPositionMode','auto');  
set(fig1,'Units','inches','Position',[0,0,10, 5]);

hold on
x_tmp = [1:1:3029];
for i = 1:10
    
    Trck = strcat(DRV, TRK_INPUT_Folder ,'\Bundle_Simluation_',num2str(i),'.txt');
    X1 = load(Trck);
    
    for t_tmp = 5:100:10000
        Den_tmp = [];
% Find the density at each time-step
        for j = 1:301
            bef = j*10 - 9;
            aft = j*10 + 9;
            Den_tmp = [Den_tmp,sum(X1(t_tmp,bef:aft))/10];
        end
        Den_tot = [Den_tot;Den_tmp];
    end
%    clr = [i*0.01, 0.5, 0.5 ];
%    plot(X1(:,4)*0.1,X1(:,1)*0.2,'Color',clr);
    
end;




%------------------------------------------------------------------------%
%                               Plot Results                             %
contourf(Den_tot,'LineColor','none');

axis([0 300 00 1000]);
%colorbar

set(gca, 'YDir','reverse')
set(gca, 'XAxisLocation', 'top')
set(gca, 'YTick', [0, 250, 500, 750, 1000])
set(gca,'yticklabel',{'0','0.5','1','1.5','2'});

hold off

set(findall(fig1,'-property','FontSize'),'FontSize',18);
set(findall(fig1,'-property','LineWidth'),'LineWidth',2);

%------------------------------------------------------------------------%
%                  Find Densities in Regions with time                   %

for t_tmp = 1:length(Den_tot(:,1))
    Den_reg = [Den_reg; [ mean(Den_tot(t_tmp,1:100)),mean(Den_tot(t_tmp,101:200)),mean(Den_tot(t_tmp,201:300)) ] ];

end


set(findall(fig1,'-property','FontSize'),'FontSize',22);
set(findall(fig1,'-property','LineWidth'),'LineWidth',2);

