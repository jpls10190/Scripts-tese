clear all
close all

% Read the image
d = dir('C:\Users\joca0\OneDrive - Universidade de Aveiro\Desktop\Uni\6ano\Projeto\Projeto\Yolo\Yolov8\datasets\crateras\images\train\*.png'); % Path to your image
indice=3;
imagePath = fullfile(d(indice).folder, d(indice).name);

image = imread(imagePath);
outputFile = strcat('C:\Users\joca0\OneDrive - Universidade de Aveiro\Desktop\Uni\6ano\Projeto\Projeto\Yolo\Yolov8\datasets\crateras\labels\txtnovos\',strcat(strrep((d(indice).name), '.png', ''),'.txt'));
fid = fopen(outputFile, 'r');

% Display the image
% figure;
% imshow(image);
% title('Click and drag to draw bounding boxes. Double-click to finish.');

hFig = figure('Toolbar','none',...
              'Menubar','none');
hIm = imshow(image);

if fid ~= -1
    % Read the file line by line
    line = fgetl(fid);
    while ischar(line)
        % Split the line by spaces or other delimiters
        parts = strsplit(line);
        rect1 = [str2double(parts{2}) str2double(parts{3}) str2double(parts{4}) str2double(parts{5})];
        if strcmp(parts{1}, '0')
            rectangle('Position', rect1, 'EdgeColor', 'g', 'LineWidth', 1);
        else
            rectangle('Position', rect1, 'EdgeColor', 'r', 'LineWidth', 1);
        end
        hold on
        % Read the next line
        line = fgetl(fid);
    end

    fclose(fid);
    end



% title('Click and drag to draw bounding boxes. Double-click to finish.');
hSP = imscrollpanel(hFig,hIm);
set(hSP,'Units','normalized',...
        'Position',[0 .1 1 .9])

% Add a magnification box and an overview tool
hMagBox = immagbox(hFig,hIm);
pos = get(hMagBox,'Position');
set(hMagBox,'Position',[0 0 pos(3) pos(4)])
imoverview(hIm)

% Initialize variables to store bounding boxes and labels
boundingBoxes = [];
labels = {};

% Ask user to draw bounding boxes
hold on;
while true
    % Get user input
    rect = getrect;
        
    % Check if the user double-clicked to finish
    if any(rect(3:end)) == 0
        break;
    end
    
    % Extracting rectangle coordinates
    x = rect(1);
    y = rect(2);
    width = rect(3);
    height = rect(4);
    x=x+width/2;
    y=y+height/2;
    
    % Normalizing coordinates
    image_size = size(image);
    normalized_x = x / image_size(2); % Normalize x coordinate
    normalized_y = y / image_size(1); % Normalize y coordinate
    normalized_width = width / image_size(2); % Normalize width
    normalized_height = height / image_size(1); % Normalize height
    
    normalized_rect=[normalized_x,normalized_y,normalized_width,normalized_height];

    % Ask user to input the label for the object
    label = inputdlg('Enter the label for the object:');

    % Draw the rectangle on the image
    if string(label) == '0' || string(label) == 'cratera'
        rectangle('Position', rect, 'EdgeColor', 'g', 'LineWidth', 1);
    elseif string(label) == '1'
        rectangle('Position', rect, 'EdgeColor', 'r', 'LineWidth', 1);
    end

    % Store bounding box and label
    boundingBoxes = [boundingBoxes; normalized_rect];
    labels = [labels; label];
end
hold off;

% Save bounding boxes and labels to a text file
fid = fopen(outputFile, 'a');
% fprintf(fid, '%s ', imagePath);
for i = 1:size(boundingBoxes, 1)
    fprintf(fid, '%s %.6f %.6f %.6f %.6f \n',labels{i}, boundingBoxes(i,:));
end
fclose(fid);

disp(strcat('Bounding boxes and labels saved to ',outputFile));